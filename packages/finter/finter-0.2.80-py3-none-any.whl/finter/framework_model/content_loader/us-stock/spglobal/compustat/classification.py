from finter.framework_model.content import Loader


class ClassificationLoader(Loader):
    def __init__(self, cm_name):
        self.__CM_NAME = cm_name
        self.__FREQ = cm_name.split(".")[-1]

    def get_df(
        self, start: int, end: int, fill_nan=True, currency=None, *args, **kwargs
    ):
        raw = self._load_cache(
            self.__CM_NAME,
            start,
            end,
            universe="us-compustat-stock",
            freq=self.__FREQ,
            fill_nan=fill_nan,
            *args,
            **kwargs,
        )

        univ = self._load_cache(
            "content.spglobal.compustat.universe.us-stock-constituent.1d",
            start,  # to avoid start dependency in dataset
            end,
            universe="us-compustat-stock",
            freq=self.__FREQ,
            fill_nan=fill_nan,
            *args,
            **kwargs,
        )

        # 컬럼명을 중복되지 않게 처리
        univ.columns = [col[:-2] for col in univ.columns]

        # 중복된 컬럼들을 그룹화하여 최대값 계산
        univ = univ.groupby(univ.columns, axis=1).max()

        # 필터 적용
        raw = raw.loc[univ.index[0] :] * univ

        return raw
