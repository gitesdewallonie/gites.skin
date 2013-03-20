Introduction
============


TODO
====

- Transformer en egg PloneZCDatetimeWidget (cf setup.py de gites.app)
    - Ou plutot integrer le code de ce 'paquet' dans gites.calendar
        - Aller retirer le XXX de gites.app quand c est fait

- Charger dans hebergement_macro automatiquement les metadata vu que les colonnes n existent plus dans la table hebergement
    - poser la question a alain pour savoir que faire avec les pictos?
    - !!! Traductions (cf gites.db content herbergement faire le meme dans metadata)
    - Ne plus utiliser hebergement_macro (en tout cas dans hebergement.pt pour l instant)
        - migrer hebEnTete vers la vue hebergement.pt
