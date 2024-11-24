from website import create_app


# app = create_app('config.TestingConfig')
app = create_app('config.ProductionConfig')
# app = create_app('config.DevelopmentConfig')


if __name__ == '__main__':
    app.run()
