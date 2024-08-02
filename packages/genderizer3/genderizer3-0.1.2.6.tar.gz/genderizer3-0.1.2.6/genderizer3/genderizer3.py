from . import tokenizer
from .classifier import Classifier
from .namesCollection import NamesCollection
from .cachedModel import CachedModel


class Genderizer(object):
    """@TODO: write docstring for Genderize"""

    initialized = False
    namesCollection = None
    classifier = None
    lang = "en"

    significantDegree = 0.3

    surelyMale = "M"
    surelyFemale = "F"
    mostlyMale = "?m"
    mostlyFemale = "?f"
    genderUnknown = "?"

    @classmethod
    def init(cls, lang="en", namesCollection=NamesCollection, classifier=None):

        cls.lang = lang
        cls.namesCollection = namesCollection

        if classifier:
            cls.classifier = classifier
        else:
            cls.classifier = Classifier(CachedModel.get(lang), tokenizer)

        cls.initialized = True

    @classmethod
    def detect(cls, firstName=None, text=None, lang=None):

        if not cls.initialized:
            cls.init()

        if cls.classifier is None:
            raise Exception("No classifier found. You need to set a classifier.")

        if cls.namesCollection is None:
            raise Exception(
                "No names collection found. You need to have names collection."
            )

        if firstName:
            nameGender = cls.namesCollection.getGender(firstName, lang)
            if nameGender:
                if nameGender["gender"] == cls.surelyMale:
                    return "male"
                elif nameGender["gender"] == cls.surelyFemale:
                    return "female"
        else:
            nameGender = None

        if text:
            probablities = dict(cls.classifier.classify(text))
            total_prob = sum(probablities.values())

            if total_prob == 0:
                return cls.genderUnknown

            classifierScoreLogF = probablities["female"] / total_prob
            classifierScoreLogM = probablities["male"] / total_prob
            classifierScoreM = classifierScoreLogF / (
                classifierScoreLogM + classifierScoreLogF
            )
            classifierScoreF = classifierScoreLogM / (
                classifierScoreLogM + classifierScoreLogF
            )

            if nameGender and nameGender["gender"].startswith("?"):
                if nameGender["gender"] == cls.mostlyMale and classifierScoreM > 0.6:
                    return "male"
                elif (
                    nameGender["gender"] == cls.mostlyFemale and classifierScoreF > 0.6
                ):
                    return "female"
                elif nameGender["gender"] != cls.genderUnknown:
                    return None

            if abs(classifierScoreF - classifierScoreM) > cls.significantDegree:
                if probablities["female"] > probablities["male"]:
                    return "female"
                else:
                    return "male"

        return cls.genderUnknown
