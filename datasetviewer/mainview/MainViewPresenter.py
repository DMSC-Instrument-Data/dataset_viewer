class MainViewPresenter(object):

    def __init__(self, mainview, *subpresenters):

        self._main_view = mainview

        for presenter in subpresenters:
            presenter.register_master(self)
