# tp_qualite_donnees

Repository du TP Qualité des données de Thomas SOHIER & Yann CLOAREC.

## Sans virtualenv

```py
pip install -r requirements.txt
```

## Virtualenv

```py
virtualenv {name}
source {name}/bin/activate
pip install -r requirements.txt
```

# Réponses questions 
## Méthodes correction erreurs du jeu de données :
Nous avons remplacé les valeurs non numériques ("0xFFFF" par exemple) par la moyenne de la veille + du lendemain. Afin d'avoir un jeu de données cohérent. 
Nous avons ensuite modifié les valeurs incohérentes, c'est à dire les valeurs ayant plus de 12°C d'écart entre la veille et le lendemain. Dans le cas du premier jour de l'année et du dernier nous afinons au seul jour dont nous possédons la donnée si l'écart entre ces deux là est de plus de 12°C.

## Les données corrigées sont elles proches des valeurs sans erreur ?
Les données corrigées sont extremement proches des valeurs sans erreur comme les graphiques le constatent. (Vous avez la possibilité de comparé le meme mois avec les deux jeux de données en cliquant sur le graphique du premier jeu et ensuite sur le graphique du meme mois du second jeu de données)

