import json

from fastapi import APIRouter, Response
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get('/', include_in_schema=False)
async def get_custom_openapi():
    with open('openapi_tech_spec.json', 'r', encoding='utf-8') as f:
        custom_openapi_json = json.load(f)
    return Response(
        content=json.dumps(custom_openapi_json, ensure_ascii=False, indent=2),
        media_type='application/json'
    )


@router.get('/docs', response_class=HTMLResponse, include_in_schema=False)
async def view_tech_spec_swagger():
    return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Technical Specification</title>
            <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
            <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
        </head>
        <body>
            <div id="swagger-ui"></div>
            <script>
                window.onload = function() {
                    SwaggerUIBundle({
                        url: '/tech_spec',
                        dom_id: '#swagger-ui',
                        presets: [SwaggerUIBundle.presets.apis, SwaggerUIBundle.SwaggerUIStandalonePreset],
                    });
                };
            </script>
        </body>
        </html>
    """


@router.get('/redoc', response_class=HTMLResponse, include_in_schema=False)
async def view_tech_spec_redoc():
    return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Technical Specification</title>
            <!-- needed for adaptive design -->
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />

            <link
            href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700"
            rel="stylesheet"
            />

            <link
            rel="shortcut icon"
            href="https://fastapi.tiangolo.com/img/favicon.png"
            />
            <!--
            ReDoc doesn't change outer page styles
            -->
            <style>
            body {
                margin: 0;
                padding: 0;
            }
            </style>
        </head>
        <body>
            <noscript>
            ReDoc requires Javascript to function. Please enable it to browse the
            documentation.
            </noscript>
            <redoc spec-url="/tech_spec"></redoc>
            <script src="https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js"></script>
        </body>
        </html>

    """
