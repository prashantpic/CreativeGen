-- Defines the schema for the 'AIModelFeedback' table.
-- Stores user feedback on outputs from specific AI models.

CREATE TABLE IF NOT EXISTS public."AIModelFeedback" (
    "id" UUID PRIMARY KEY NOT NULL,
    "userId" UUID NOT NULL,
    "generationRequestId" UUID,
    "modelVersionId" UUID,
    "rating" INTEGER CHECK ("rating" >= 1 AND "rating" <= 5),
    "comment" TEXT,
    "feedbackTimestamp" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "details" JSONB,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "fk_aimodelfeedback_user" FOREIGN KEY ("userId") REFERENCES public."User"("id") ON DELETE SET NULL ON UPDATE NO ACTION,
    CONSTRAINT "fk_aimodelfeedback_genrequest" FOREIGN KEY ("generationRequestId") REFERENCES public."GenerationRequest"("id") ON DELETE SET NULL ON UPDATE NO ACTION,
    CONSTRAINT "fk_aimodelfeedback_modelversion" FOREIGN KEY ("modelVersionId") REFERENCES public."AIModelVersion"("id") ON DELETE SET NULL ON UPDATE NO ACTION
);

-- Indexes for the AIModelFeedback table
CREATE INDEX IF NOT EXISTS "idx_aimodelfeedback_userid" ON public."AIModelFeedback" USING btree ("userId");
CREATE INDEX IF NOT EXISTS "idx_aimodelfeedback_generationrequestid" ON public."AIModelFeedback" USING btree ("generationRequestId");
CREATE INDEX IF NOT EXISTS "idx_aimodelfeedback_modelversionid" ON public."AIModelFeedback" USING btree ("modelVersionId");

COMMENT ON TABLE public."AIModelFeedback" IS 'User feedback on outputs from specific AI models.';
COMMENT ON COLUMN public."AIModelFeedback"."generationRequestId" IS 'Link to the specific generation request the feedback is about.';
COMMENT ON COLUMN public."AIModelFeedback"."modelVersionId" IS 'Link to the model version the feedback pertains to.';
COMMENT ON COLUMN public."AIModelFeedback"."rating" IS 'Optional rating (e.g., 1-5 stars).';
COMMENT ON COLUMN public."AIModelFeedback"."details" IS 'Additional structured feedback data.';