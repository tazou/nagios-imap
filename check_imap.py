#!/usr/bin/env python2
# coding: utf-8

# Guillaume DUALÉ - 20181114
# Script permettant de compter le nombre de mail totaux (lus et non lus) sur une boite imap
# Affiche l'information et renvoi les codes retour pour Nagios.

import imaplib
import sys
import argparse

# Parser les arguments de la ligne de commande
parser = argparse.ArgumentParser()
parser.add_argument("imap_server", help="Serveur IMAP")
parser.add_argument("imap_port", help="Port du serveur IMAP")
parser.add_argument("imap_folder", help="Nom du dossier IMAP : Exemple : INBOX")
parser.add_argument("imap_user", help="Identifiant IMAP")
parser.add_argument("imap_password", help="Mot de passe IMAP")
parser.add_argument("threshold_warning", help="Nombre de mail pour WARNING",type=int)
parser.add_argument("threshold_critical", help="Nombre de mail pour CRITICAL", type=int)
args = parser.parse_args()

# Fonction pour quiter imap : close connexion et logout
def quit_imap():
    mail.close()
    mail.logout()

# Construire les variables pour la connexion imap avec les arguments de la ligne de commande.
FROM_EMAIL  = args.imap_user
FROM_PWD    = args.imap_password
SMTP_SERVER = args.imap_server
SMTP_PORT   = args.imap_port

# Créer la connexion imap
mail = imaplib.IMAP4_SSL(SMTP_SERVER)
mail.login(FROM_EMAIL,FROM_PWD)
mail.select(args.imap_folder)

# Lire les mails et les compter
typ, data = mail.search(None, 'ALL')
nb_mail = (len(data[0].split()))
print "Nombre de mail(s) dans la boite : {}".format(nb_mail)

# Tests de seuils pour Nagios
if nb_mail > args.threshold_critical:
    print "CRITICAL ! {} mails".format(nb_mail)
    quit_imap()
    sys.exit(2)
if nb_mail > args.threshold_warning:
    print "WARNING ! {} mails".format(nb_mail)
    quit_imap()
    sys.exit(1)

# Si l'on ne rentre pas dans les précédents "if", les seuils sont OK, on sort en exit 0
quit_imap()
sys.exit(0)
