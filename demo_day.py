import logging
import random
import time

import models as mdl

CHAT_DEMO = [("Quels sont les principaux articles écrits dans le domaine du machine learning dans les 6 derniers mois ?",
              """Voici les principaux articles écrits dans le domaine du machine learning dans les 6 derniers mois :
             
- Programmez! 267 (page 69) - Janvier 2025
- Programmez! Hors-Série 14 (pages 60, 61, 62) - Mars 2024
- Programmez! 264 (pages 6, 7, 8, 9) - Juillet 2024
- Programmez! 261 (pages 71, 72, 73) - Janvier 2024
 
Si tu souhaites des informations plus détaillées sur un article en particulier, n'hésite pas à me le faire savoir."""),
             ("Je souhaite un résumé pour chacun des articles.", """Voici les résumés des articles demandés :

**Programmez! 267 (page 69) - Janvier 2025**

Le machine learning est une discipline en constante évolution. Cet article explore les dernières avancées dans le domaine, en mettant en lumière les nouvelles techniques et les outils qui révolutionnent la manière dont les données sont analysées et interprétées. Les auteurs discutent des applications pratiques du machine learning dans divers secteurs, tels que la santé, la finance et l'industrie. Ils soulignent également les défis éthiques et techniques associés à l'utilisation de ces technologies, ainsi que les perspectives d'avenir pour le développement de modèles plus performants et plus fiables.

**Programmez! Hors-Série 14 (pages 60, 61, 62) - Mars 2024**

Cet article se concentre sur l'intégration du machine learning dans les systèmes de gestion de données. Il présente des cas d'utilisation concrets où le machine learning permet d'améliorer l'efficacité et la précision des analyses de données. Les auteurs détaillent les étapes nécessaires pour mettre en œuvre des solutions de machine learning, en insistant sur l'importance de la qualité des données et de la sélection des algorithmes appropriés. Ils abordent également les défis liés à la mise en œuvre de ces technologies, tels que la gestion des biais et la sécurité des données.

**Programmez! 264 (pages 6, 7, 8, 9) - Juillet 2024**

Cet article examine les tendances actuelles en matière de machine learning, en se concentrant sur les innovations technologiques qui transforment le paysage du développement logiciel. Les auteurs discutent des nouvelles architectures de modèles, des frameworks de développement et des outils de visualisation qui facilitent l'utilisation du machine learning. Ils mettent en avant les avantages de l'automatisation des processus de développement et les opportunités offertes par l'intelligence artificielle pour améliorer la productivité et l'innovation. L'article se termine par une réflexion sur les compétences nécessaires pour les développeurs afin de rester compétitifs dans un marché en constante évolution.

**Programmez! 261 (pages 71, 72, 73) - Janvier 2024**

Cet article explore les applications du machine learning dans le domaine de la santé. Il présente des études de cas où le machine learning est utilisé pour améliorer le diagnostic des maladies, la personnalisation des traitements et la gestion des données médicales. Les auteurs discutent des défis éthiques et techniques associés à l'utilisation du machine learning dans la santé, tels que la confidentialité des données et la transparence des algorithmes. Ils soulignent également l'importance de la collaboration entre les professionnels de la santé et les experts en machine learning pour développer des solutions innovantes et efficaces. """),
             ("Que trouve-t-on dans le hors-série de mars 2024 ?",
              """Dans le hors-série de mars 2024, on trouve des articles sur la traduction automatique et la classification d'articles. Les articles abordent l'utilisation de modèles de traduction automatique pour traduire des textes d'une langue à une autre, notamment du japonais à l'anglais et de l'anglais au français, en utilisant des outils comme MarianMT et des tokenizers spécifiques. 

Ils expliquent également comment classer des articles traduits en différentes catégories telles que la politique, le sport, la culture, l'économie, et les affaires internationales, en utilisant des modèles de classification comme BART. Les articles incluent des exemples de code et des explications détaillées sur les étapes de traduction et de classification. 

[Programmez! hors-série 14 (pages 11, 12, 13) - Mars 2024]"""),
             ("Merci.", """Avec plaisir ! Si tu as d'autres questions ou besoin de plus d'informations, n'hésite pas à demander.""")]

QUIZ_DEMO = [
    '''
{
    "topic":"Machine Learning",
    "questions":[
        {
            "question":"Quel algorithme de machine learning est souvent utilisé pour les tâches de classification sans nécessiter de programmation complexe ?",
            "choices":[
                "Deep Learning",
                "Réseaux de neurones",
                "Random Forest",
                "SVM"
            ],
            "answer":"Random Forest",
            "origin":"Programmez! Hors-série 14 (page 69) - Janvier 2025",
            "explain":"La Random Forest est un algorithme de machine learning populaire pour les tâches de classification. Il est facile à utiliser et ne nécessite pas de programmation complexe, ce qui en fait un choix courant pour les développeurs débutants."
        },
        {
            "question":"Quel outil permet de créer et d'entraîner des modèles de machine learning sans écrire de code ?",
            "choices":[
                "TensorFlow",
                "PyTorch",
                "Teachable Machine",
                "Scikit-Learn"
            ],
            "answer":"Teachable Machine",
            "origin":"Programmez! 264 (pages 46, 47, 48) - Juillet 2024",
            "explain":"La Teachable Machine est un outil développé par Google qui permet de créer et d'entraîner des modèles de machine learning via une interface web, sans écrire de code."
        },
        {
            "question":"Quelle bibliothèque Python est souvent utilisée pour la manipulation et l'analyse des données dans les projets de machine learning ?",
            "choices":[
                "TensorFlow",
                "Pandas",
                "Keras",
                "Scikit-Learn"
            ],
            "answer":"Pandas",
            "origin":"Programmez! Hors-série 14 (pages 66, 67) - Janvier 2025",
            "explain":"Pandas est une bibliothèque Python puissante pour la manipulation et l'analyse des données, souvent utilisée dans les projets de machine learning pour préparer et nettoyer les données."
        },
        {
            "question":"Quel type de modèle de machine learning est souvent utilisé pour les tâches de traitement du langage naturel (NLP) ?",
            "choices":[
                "Modèles de régression",
                "Modèles de classification",
                "Modèles de clustering",
                "Modèles de génération de langage"
            ],
            "answer":"Modèles de génération de langage",
            "origin":"Programmez! Hors-série 14 (pages 60, 61, 62) - Mars 2024",
            "explain":"Les modèles de génération de langage sont souvent utilisés pour les tâches de traitement du langage naturel (NLP), permettant aux machines de comprendre, interpréter et générer du langage humain."
        },
        {
            "question":"Quel concept est essentiel pour garantir la reproductibilité des expériences de machine learning ?",
            "choices":[
                "Data Version Control",
                "Machine Learning Ops",
                "Deep Learning",
                "Transfer Learning"
            ],
            "answer":"Data Version Control",
            "origin":"Programmez! 261 (pages 72, 73) - Janvier 2024",
            "explain":"Data Version Control (DVC) est un outil open source qui permet de versionner les données, les modèles et les pipelines de machine learning, garantissant ainsi la reproductibilité des expériences."
        }
    ]
}
    ''',
    '''
{
    "topic":"Aspects Métiers et Business pour Développeurs",
    "questions":[
        {
            "question":"Quel est le principal objectif de l'intégration des outils NoCode/LowCode dans le développement d'applications ?",
            "choices":[
                "Réduire les coûts de développement",
                "Soutenir les nouveaux développeurs",
                "Améliorer la qualité du code",
                "Accélérer le développement applicatif"
            ],
            "answer":"Accélérer le développement applicatif",
            "origin":"Programmez! 265 (pages 28, 29) - Août 2024",
            "explain":"L'intégration des outils NoCode/LowCode vise à accélérer le développement applicatif en permettant aux développeurs de créer des applications fonctionnelles rapidement, sans avoir besoin d'écrire du code complexe."
        },
        {
            "question":"Quelle est une des principales opportunités offertes par les outils NoCode/LowCode pour les développeurs traditionnels ?",
            "choices":[
                "Réduire les coûts de développement",
                "Améliorer la qualité du code",
                "Élargir leur éventail de compétences",
                "Accélérer le développement applicatif"
            ],
            "answer":"Élargir leur éventail de compétences",
            "origin":"Programmez! 265 (pages 28, 29) - Août 2024",
            "explain":"Les outils NoCode/LowCode offrent aux développeurs traditionnels l'opportunité d'élargir leurs compétences en leur permettant de travailler sur des projets sans code, tout en restant pertinents dans une industrie en constante évolution."
        },
        {
            "question":"Quel est le rôle principal des interfaces visuelles dans les outils NoCode/LowCode ?",
            "choices":[
                "Réduire les coûts de développement",
                "Faciliter la collaboration entre développeurs et non-développeurs",
                "Améliorer la qualité du code",
                "Accélérer le développement applicatif"
            ],
            "answer":"Faciliter la collaboration entre développeurs et non-développeurs",
            "origin":"Programmez! 265 (pages 28, 29) - Août 2024",
            "explain":"Les interfaces visuelles dans les outils NoCode/LowCode facilitent la collaboration entre développeurs et non-développeurs en introduisant un vocabulaire partagé, permettant ainsi une meilleure compréhension et contribution de tous les acteurs impliqués."
        },
        {
            "question":"Pourquoi les outils NoCode/LowCode sont-ils considérés comme un atout pour les non-développeurs ?",
            "choices":[
                "Ils permettent de réduire les coûts de développement",
                "Ils facilitent la création d'applications sans compétences en codage",
                "Ils améliorent la qualité du code",
                "Ils accélèrent le développement applicatif"
            ],
            "answer":"Ils facilitent la création d'applications sans compétences en codage",
            "origin":"Programmez! 265 (pages 28, 29) - Août 2024",
            "explain":"Les outils NoCode/LowCode permettent aux non-développeurs de créer des applications sans avoir besoin de compétences en codage, en utilisant des interfaces visuelles et des bibliothèques de composants pré-construits."
        },
        {
            "question":"Quelle est une des principales caractéristiques des outils NoCode/LowCode en termes de fonctionnalités ?",
            "choices":[
                "Automatisation des flux de travail",
                "Réduction des coûts de développement",
                "Amélioration de la qualité du code",
                "Accélération du développement applicatif"
            ],
            "answer":"Automatisation des flux de travail",
            "origin":"Programmez! 265 (pages 28, 29) - Août 2024",
            "explain":"Les outils NoCode/LowCode sont caractérisés par l'automatisation des flux de travail, permettant aux utilisateurs de construire des applications en glissant et en déposant des éléments sur un canevas, définissant ainsi la structure et la disposition de l'application de manière simple et compréhensible."
        }
    ]
}'''
]


def delay(passthrough: str) -> str:
    alea = random.uniform(1, 3)
    time.sleep(alea)
    return passthrough


def mocked_chat(question: str) -> str:
    for challenge, answer in CHAT_DEMO:
        logging.info(f"{challenge}")
        if challenge.lower() == question.lower():
            logging.info(f"{answer}")
            return delay(answer)

    return None


def mocked_quiz(which: int) -> str:
    which %= len(QUIZ_DEMO)
    logging.info(f"Quiz {which}: {QUIZ_DEMO[which]}")
    return delay(mdl.Quiz.model_validate_json(QUIZ_DEMO[which]))
