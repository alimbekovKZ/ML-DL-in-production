from sklearn import svm
from sklearn import datasets
from bentoml import env, artifacts, api, BentoService
from bentoml.adapters import DataframeInput
from bentoml.frameworks.sklearn import SklearnModelArtifact
from bentoml.adapters import DataframeInput
from bentoml.artifact import SklearnModelArtifact

from bentoml import (env,               #среда
                     artifacts,         # артифакты
                     api,               # общение с API
                     BentoService,      # сервис для модели
                     web_static_content # статичный контент
                     )

@env(auto_pip_dependencies=True)
@artifacts([SklearnModelArtifact('model')])     
@web_static_content('./static')                 
class Classifier(BentoService):

    @api(input=DataframeInput(), batch=True)
    def test(self, df):
        return self.artifacts.model.predict(df)


if __name__ == "__main__":
    # Загрузим датасет и обучим простую модель
    iris = datasets.load_iris()
    X, y = iris.data, iris.target
    clf = svm.SVC(gamma='scale')
    clf.fit(X, y)

    # Инициализируем класс классификатора
    iris_classifier_service = Classifier()

    # Закинем модель в артифакт
    iris_classifier_service.pack('model', clf)

    # Сохраним и запустим
    saved_path = iris_classifier_service.save()
