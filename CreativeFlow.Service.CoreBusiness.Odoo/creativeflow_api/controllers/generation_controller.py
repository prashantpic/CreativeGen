import json
import logging
from odoo import http, _, fields
from odoo.http import request
from odoo.exceptions import UserError, AccessError, ValidationError

_logger = logging.getLogger(__name__)

class GenerationController(http.Controller):

    def _json_response(self, data, status=200):
        return request.make_response(
            json.dumps(data),
            headers=[('Content-Type', 'application/json')],
            status=status
        )

    @http.route('/api/v1/generation/create', type='json', auth='user', methods=['POST'], csrf=False)
    def initiate_generation(self, **kwargs):
        """
        API endpoint to initiate an AI creative generation task.
        It validates the request, deducts credits, creates a tracking record,
        and publishes a job to a message broker.
        """
        try:
            user = request.env.user
            params = request.jsonrequest
            
            prompt = params.get('prompt')
            project_id = params.get('project_id')
            if not all([prompt, project_id]):
                raise ValidationError(_("'prompt' and 'project_id' are required fields."))

            # --- Validation and Cost Calculation ---
            # For simplicity, let's assume a fixed cost. A real implementation
            # would calculate this based on parameters (e.g., resolution, format).
            credit_cost = 1.0 

            # --- Critical Section: Credit Deduction and Request Creation ---
            with request.env.cr.savepoint():
                # Deduct credits first
                user.deduct_credits(credit_cost, f"AI Generation Request for project ID {project_id}")

                # Create the generation request record
                generation_request = request.env['creativeflow.generation_request'].create({
                    'project_id': project_id,
                    'prompt': prompt,
                    'status': 'pending',
                })

            # --- Publish Job to RabbitMQ ---
            publisher = request.env['rabbitmq.publisher']
            job_payload = {
                'generation_request_id': generation_request.id,
                'user_id': user.id,
                'project_id': project_id,
                'prompt': prompt,
                'params': params, # Pass all original params
            }
            publisher.publish_generation_job(job_payload)

            _logger.info("Successfully queued generation job %s for user %s", generation_request.id, user.name)
            return {
                'status': 'success',
                'message': 'Generation request queued successfully.',
                'generation_id': generation_request.id,
            }

        except (UserError, ValidationError) as e:
            _logger.warning("Generation request validation failed for user %s: %s", request.env.user.name, e)
            return self._json_response({'error': 'validation_error', 'message': str(e)}, status=422)
        except AccessError as e:
            _logger.warning("Generation request access error for user %s: %s", request.env.user.name, e)
            return self._json_response({'error': 'access_denied', 'message': "You do not have access to this resource."}, status=403)
        except Exception as e:
            _logger.exception("An unexpected error occurred during generation initiation.")
            return self._json_response({'error': 'server_error', 'message': 'An internal server error occurred.'}, status=500)

    @http.route('/api/v1/generation/<int:generation_id>/status', type='http', auth='user', methods=['GET'], csrf=False)
    def get_generation_status(self, generation_id, **kwargs):
        """
        API endpoint to fetch the status of a specific generation request.
        """
        try:
            # Sudo to find the record, then check access rights
            generation_request = request.env['creativeflow.generation_request'].sudo().browse(generation_id)
            if not generation_request.exists():
                return self._json_response({'error': 'not_found', 'message': 'Generation request not found.'}, status=404)

            # Security check: ensure the current user owns this request
            if generation_request.user_id.id != request.env.user.id:
                 raise AccessError(_("You are not allowed to view this generation request."))

            response_data = {
                'id': generation_request.id,
                'status': generation_request.status,
                'created_at': fields.Datetime.to_string(generation_request.create_date),
                'error_message': generation_request.error_message or None,
                # In a real scenario, you'd include URLs to sample/final assets if ready
                # 'results': [{'url': asset.url} for asset in generation_request.result_asset_ids]
            }
            return self._json_response(response_data)
        
        except AccessError as e:
            return self._json_response({'error': 'access_denied', 'message': str(e)}, status=403)
        except Exception as e:
            _logger.exception("Error fetching generation status for ID %s.", generation_id)
            return self._json_response({'error': 'server_error', 'message': 'An internal server error occurred.'}, status=500)