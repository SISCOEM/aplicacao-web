def handle_error(get_response):
    def middleware(request):
        try:
            response = get_response(request)
        except Exception as e:
            import traceback
            from django.core.mail import mail_admins

            trace_info = '\n'.join(traceback.format_exception(
                etype=type(e),
                value=e,
                tb=e.__traceback__,
            ))

            mail_admins(
                'Erro no servidor',
                trace_info,
                fail_silently=False,
            )

            # Re-raise the exception to let it propagate
            raise

        return response

    return middleware