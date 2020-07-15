import japronto
import logger
from handlers import calc_handler, login_handler, refresh_handler, error_handler

if __name__ == '__main__':
    logger.Logger().log('Start application')
    app = japronto.Application()

    app.router.add_route('/calc', calc_handler.calc_handler, "GET")
    app.router.add_route('/login', login_handler.login_handler, "POST")
    app.router.add_route('/refresh', refresh_handler.refresh_handler, "POST")

    error_handler.add_error_handler(app)
    # add protection from data race
    app.run(worker_num=8)
    # app.run()
