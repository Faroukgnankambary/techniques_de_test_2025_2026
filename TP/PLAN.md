L'objet du TP sera la réalisation d'un micro-service de triangulation. Mais Pour ce faire nous débutons par la mise en place et la réalisation des tests.

##Plan de Test

1.	Objectifs des tests

L’objectif est de décrire la stratégie de test du micro-service Triangulator, chargé de calculer la triangulation d’ensembles de points récupérés depuis le service PointSetManager en garantissant les interactions, la performance, la robustesse et la conformité API du composant.



2.	Organisation des tests

Globalement les tests porteront sur :
•	Le code de conversion binaire et interne entre structures PointSet et Triangles
•	L’algorithme de triangulation interne
•	L’API HTTP exposée par le service Flask
•	Les interactions externes avec le PointSetManager
•	Les performances (triangulation et conversion)
•	La qualité (linting, documentation, couverture)



3.	Types des tests
   
3.1.	Tests unitaires

•	Objectif : Valider le comportement isolé de chaque fonction interne du composant.

•	Outils : Pytest

•	Cas Prévus : 

Catégorie	                       Cas de test	                                               Résultat attendu
Conversion binaire           	PointSet -> bytes -> PointSet	                               L’objet reconverti est identique à l’original
Conversion binaire	          Triangles -> bytes -> Triangles	                             Données identiques à l’entrée
Validation des entrées	      PointSet vide                                                Exception / code d’erreur approprié
Validation des entrées	      Coordonnées non valides (NaN, inf, négatif)	                 Exception
Triangulation                 Ensemble simple (3 points)                                   1 triangle correct
Triangulation                 Ensemble complexe (n points)	                               Triangles valides, pas de chevauchement
Triangulation	                Points colinéaires	                                         Erreur ou 0 triangle


3.2.	Tests d’intégration / API

•	Objectif : Vérifier le bon comportement global du service Flask 

•	Outils : pytest + FlaskClient 

•	Cas prévus :

Endpoints	                     Scénario	                                                   Résultats attendus
POST /triangulate	            ID valide	                                               Code 200 + résultat binaire valide
POST /triangulate	            ID inexistant	                                           Code 404
POST /triangulate	            Format invalide	                                         Code 400
GET /health	                  Vérification service	                                   Code 200 + “ok”
Communication externe	        Timeout du PointSetManager	                             Code 503 + message clair


3.3.	Tests de performance

•	Objectif : Mesurer le temps d’exécution de la triangulation et de la (dé)sérialisation.

•	Outils : pytest avec marqueur @pytest.mark.perf

•	Métriques : 

Test	                          Données	Attentes
Triangulation rapide	          10 points	< 0.05 s
Triangulation moyenne	          100 points	< 0.5 s
Conversion binaire	            1000 points	< 0.1 s
Stress test	10000 points	      Temps mesuré, pas forcément validé
Les tests de performance seront exclus par défaut (make unit_test) et activables par make perf_test.



3.4.	Tests de conformité / qualité

•	Objectif : Vérifier la qualité du code, sa documentation et sa couverture.

•	Outils
	ruff : lint
	pdoc3 : documentation
	coverage : rapport de couverture

•	Commandes Makefile : 
Commande	                                  Description
make test	                              Lance tous les test
make unit_test	                        Tests sans performance
make perf_test	                        Tests de performance
make coverage	                          Rapport HTML de couverture
make lint	                              Vérifie la qualité du code
make doc	                             Génère la documentation HTML


4.	Critères de réussite

•	Tous les tests passent (pytest green)
•	Couverture > 90%
•	ruff check sans erreur
•	pdoc3 génère la doc complète
•	Temps de test total < 10 secondes
•	Aucune dépendance externe non autorisée

