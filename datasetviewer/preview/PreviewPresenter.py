class PreviewPresenter(object):

    def __init__(self, view, source):

        if view is None:
            raise ValueError("Error: Cannot create Presenter when View is None.")

        if source is None:
            raise ValueError("Error: Cannot create Presenter when Source is None.")

        self._view = view
        self._source = source
