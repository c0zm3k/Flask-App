def register_filters(app):
    @app.template_filter('datefmt')
    def datefmt(value, fmt='%Y-%m-%d %H:%M'):
        try:
            return value.strftime(fmt)
        except Exception:
            return value
