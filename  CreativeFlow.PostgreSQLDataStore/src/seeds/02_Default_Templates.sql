-- Seeds default creative templates into the 'Template' table.
-- These templates are available to all users.
-- This script is designed to be idempotent, assuming template names are unique for public templates.

-- Template 1: Instagram Story Ad
INSERT INTO public."Template" (
    "id",
    "userId",
    "name",
    "description",
    "category",
    "previewUrl",
    "sourceData",
    "tags",
    "isPublic",
    "createdAt",
    "updatedAt"
) VALUES (
    gen_random_uuid(),
    NULL,
    'Instagram Story Ad',
    'A vibrant, eye-catching template for Instagram Story advertisements, optimized for vertical video and engagement.',
    'Social Media',
    'minio/previews/instagram_story_ad.jpg',
    '{"version": "1.0", "dimensions": "1080x1920", "elements": [{"type": "background", "color": "#FDEB71"}, {"type": "text", "content": "Your Catchy Headline Here", "font": "Arial", "size": 96, "position": [50, 200]}, {"type": "placeholder", "name": "product_image", "position": [50, 600], "size": [800, 800]}, {"type": "cta", "text": "Swipe Up!", "position": [50, 1700]}]}',
    '["instagram", "story", "video", "ad", "marketing", "social"]',
    true,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
)
ON CONFLICT (name) DO NOTHING;

-- Template 2: Facebook Carousel Post
INSERT INTO public."Template" (
    "id",
    "userId",
    "name",
    "description",
    "category",
    "previewUrl",
    "sourceData",
    "tags",
    "isPublic",
    "createdAt",
    "updatedAt"
) VALUES (
    gen_random_uuid(),
    NULL,
    'Facebook Carousel Post',
    'A multi-card carousel template for Facebook, perfect for showcasing multiple products, features, or story points.',
    'Social Media',
    'minio/previews/facebook_carousel_post.jpg',
    '{"version": "1.0", "dimensions": "1080x1080", "card_count": 3, "elements_per_card": [{"type": "image", "name": "card_image"}, {"type": "text", "name": "card_title", "size": 48}, {"type": "text", "name": "card_description", "size": 24}]}',
    '["facebook", "carousel", "ad", "multi-product", "ecommerce"]',
    true,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
)
ON CONFLICT (name) DO NOTHING;

-- Template 3: LinkedIn Article Banner
INSERT INTO public."Template" (
    "id",
    "userId",
    "name",
    "description",
    "category",
    "previewUrl",
    "sourceData",
    "tags",
    "isPublic",
    "createdAt",
    "updatedAt"
) VALUES (
    gen_random_uuid(),
    NULL,
    'LinkedIn Article Banner',
    'A professional and clean banner template for LinkedIn articles to grab the attention of a professional audience.',
    'Blog',
    'minio/previews/linkedin_article_banner.jpg',
    '{"version": "1.0", "dimensions": "1920x1080", "elements": [{"type": "background", "image_url": "placeholder.jpg", "overlay_opacity": 0.5}, {"type": "text", "content": "Professional Article Title", "font": "Helvetica", "size": 120, "color": "#FFFFFF", "position": [100, 540]}]}',
    '["linkedin", "blog", "article", "banner", "professional", "business"]',
    true,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
)
ON CONFLICT (name) DO NOTHING;