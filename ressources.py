#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Tables de correspondance

    Cette liste est à manipuler avec le plus grand soin car elle doit correspondre exactement aux champs ACF cible des caractéristiques LMB

"""

__author__ = 'lgp'


marque = {
	"Audio Service" : "audio_service",
	"Beltone" : "beltone",
	"Bernafon" : "bernafon",
	"Biotone" : "biotone",
	"Biotone Rexton" : "biotone_rexton",
	"Coselgi appareil auditif" : "coselgi appareil auditif",
	"Hansaton - Audiomedi" : "hansaton_audiomedi",
	"Hansaton" : "hansaton",
	"Interton" : "interton",
	"Newson" : "newson",
	"Oticon" : "oticon",
	"Phonak" : "phonak",
	"Resound" : "resound",
	"Rexton" : "rexton",
	"Siemens" : "siemens",
	"Sona" : "sona",
	"Sonic Innovations" : "sonic_innovations",
	"Sonic Innovation" : "sonic_innovations",
	"Starkey" : "starkey",
	"Unitron Hearing" : "unitron_hearing",
	"Unitron" : "unitron_hearing",
	"Widex" : "widex",
	"Autre" : "autre",
}

type_appareil = {
	"Branche de lunette" : "branche_de_lunette",
	"Branche de lunette auditive" : "branche_de_lunette_auditive",
	"Contour d'oreille" : "contour_d_oreille",
	"Contour d'oreille standard" : "contour_d_oreille_standard",
	"Contour écouteur déporté" : "contour_ecouteur_deporte",
	"Intra classique" : "intra_classique",
	"Intra très discret" : "intra_tres_discret",
	"Intra-auriculaire" : "intra_auriculaire",
	"Intra-auriculaire discret" : "intra_auriculaire_discret",
	"Intra-auriculaire très discret" : "intra_auriculaire_tres_discret",
	"Intraauriculaire classique" : "intra_auriculaire_classique",
	"Micro contour d'oreille" : "micro_contour_d_oreille",
	"Micro contour open" : "micro_contour_open",
	"Micro contour standard" : "micro_contour_standard",
	"Micro contour écouteur déporté" : "micro_contour_ecouteur_deporte",
	"Micro contour à écouteur déporté" : "micro_contour_ecouteur_deporte",
	"appareil auditif invisible" : "appareil_auditif_invisible",
	"appareil auditif très discret" : "appareil_auditif_tres_discret",
	"intra CIC micro déporté" : "intra_cic_micro_deporte",
	"intra conduit micro déporté" : "intra_conduit_micro_deporte",
	"intra invisible" : "intra_invisible",
}


degre_perte={
	"Surdité légere : de 20 à 40 % de perte" : "surdite_legere_de_20_a_40_de_perte",
	"Surdité légere" : "surdite_legere",
	"Surdité légère" : "surdite_legere",
	"Surdité légere à moyenne" : "surdite_legere_a_moyenne",
	"Surdité légère à moyenne" : "surdite_legere_a_moyenne",
	"Surdité légere à moyenne de 20 à 70 % de perte" : "surdite_legere_a_moyenne_de_20_a_70_de_perte",
	"Surdité légere à sévère" : "surdite_legere_a_severe",
	"Surdité légére à sévère" : "surdite_legere_a_severe",
	"Surdité légere à sévère de 20 à 90% de perte" : "surdite_legere_a_severe_de_20_a_90_de_perte",
	"surdité moyenne à profonde de 40 à + de 90 % de perte  " : "surdite_moyenne_a_profonde_de_40_a_plus_de_90_de_perte",
	"Surdité moyenne à sévère" : "surdite_moyenne_a_severe",
	"Surdité moyenne à sévère de 40 à 90 % de perte" : "surdite_moyenne_a_severe_de_40_a_90_de_perte",
	"Surdité moyenne de 40 à 70 %" : "surdite_moyenne_de_40_a_70",
	"Surdité profonde" : "surdite_profonde",
	"Surdité profonde + de 90 % de perte auditive moyenne" : "surdite_profonde_plus_de_90_de_perte_auditive_moyenne",
	"Surdité sévère à profonde" : "surdite_severe_a_profonde",
	"Surdité sévère à profonde de 70 à + de 90% de perte" : "surdite_severe_a_profonde_de_70_a_plus_de_90_de_perte",
	"Surdité sévère de 70 à 90 %" : "surdite_severe_de_70_a_90",
}



gamme = {
	"Confort" : "confort",
	"Elite" : "elite",
	"Excellence" : "excellence",
	"Extra" : "extra",
	"Optimum" : "optimum",
	"Premier" : "premier",
}


classe={
	"Classe A" : "classe_a",
	"Classe B" : "classe_b",
	"Classe C" : "classe_c",
	"Classe D" : "classe_d",
}

date_sortie= {
	"Avant 2011" : "2011_avant",
	"Début 2012" : "2012_debut",
	"Fin 2012" : "2012_fin",
	"Mi 2012" : "2012_mi",
	"2013" : "2013",
	"Début 2013" : "2013_debut",
	"Fin 2013" : "2013_fin",
	"Mi 2013" : "2013_mi",
	"2014" : "2014",
	"Début 2014" : "2014_debut",
	"Fin 2014" : "2014_fin",
	"2015" : "2015",
	"Début 2015" : "2015_debut",
	"Fin 2015" : "2015_fin",
	"2016" : "2016",
	"Début 2016" : "2016_debut",
	"Fin 2016" : "2016_fin",
	"Mi 2016" : "2016_mi",
	"Début 2017" : "2017_debut",
	"Fin 2017" : "2017_fin",
	"Mi 2017" : "2017_mi",
	"2018" : "2018",
	"Début 2018" : "2018_debut",
	"Mi 2018" : "2018_mi",
	"Fin 2018" : "2018_fin",	
}


telecommande={
	"oui" : "oui",
	"oui avec télécommande uniquement" : "oui_telecommande",
	"non" : "non",
}


bluetooth={
	"oui" : "oui",
	"non" : "non",
}

multiprogramme = {
	"oui" : "oui",
	"oui avec télécommande uniquement" : "oui_telecommande",
	"non" : "non",
}

reglage_volume={
	"oui" : "oui",
	"oui avec télécommande uniquement" : "oui_telecommande",
	"non" : "non",
}


prothese_auditive_rechargeable = {
	"oui" : "oui",
	"non" : "non",
}

microphone = {
	"oui" : "oui",
	"non" : "non", 
	"optionnels" : "optionnels",
}

modele_piles={
	"10" : "10",
	"13" : "13",
	"312" : "312",
	"675" : "675",
	"Accu Type 10" : "accu_type_10",
	"Accu Type 13" : "accu_type_13",
	"Accu Type 312" : "accu_type_312",
	"Large bande" : "large_bande",
	"Systéme Channel Free" : "systeme_channel_free",
}


systeme_anti_acouphenes = {
	"oui" : "oui",
	"non" : "non",
}

precision_canaux= {
	"2 canaux" : "2_canaux",
	"3 canaux" : "3_canaux",
	"4 canaux" : "4_canaux",
	"5 canaux" : "5_canaux",
	"6 canaux" : "6_canaux",
	"7 canaux" : "7_canaux",
	"8 canaux" : "8_canaux",
	"9 canaux" : "9_canaux",
	"10 canaux" : "10_canaux",
	"11 canaux" : "11_canaux",
	"12 canaux" : "12_canaux",
	"13 canaux" : "13_canaux",
	"14 canaux" : "14_canaux",
	"15 canaux" : "15_canaux",
	"16 canaux" : "16_canaux",
	"17 canaux" : "17_canaux",
	"18 canaux" : "18_canaux",
	"20 canaux" : "20_canaux",
	"24 canaux" : "24_canaux",
	"Systéme Channel Free" : "systeme_channel_free",
	"Large bande" : "large_bande",
}

synchro_binaurale = {
	"oui" : "oui",
	"non" : "non",
}


caracteristiques_id_name={
    "ACC-000000-00001" : "Type",
    "ACC-000000-00006" : "Gamme",
    "ACC-000000-00008" : "Degré de perte auditive",
    "ACC-000000-0000b" : "Classification Sécurité Sociale",
    "ACC-000000-0000c" : "Marque",
    "ACC-000000-0000d" : "Compatibilité Télécommande",
    "ACC-000000-0000e" : "Audioprothese bluetooth",
    "ACC-000000-0000f" : "Multi programmes",
    "ACC-000000-0000g" : "Réglage du volume",
    "ACC-000000-0000h" : "Prothese auditive rechargeable",
    "ACC-000000-0000i" : "Microphones directionnels",
    "ACC-000000-0000j" : "Modéle de pile",
    "ACC-000000-0000k" : "Système Anti Acouphènes",
    "ACC-000000-0000l" : "Site Fabriquant",
    "ACC-000000-0000m" : "Précision réglages audioprothétiques",
    "ACC-000000-0000n" : "Synchronisation Binaurale",
    "ACC-000000-0000o" : "Liens vidéo",
    "ACC-000000-0000p" : "Partager ce site avec vos amis",
    "ACC-000000-0000q" : "Date de sortie"
}

caracteristiques_id_lmb2wp={
    "ACC-000000-00001" : type_appareil,
    "ACC-000000-00006" : gamme,
    "ACC-000000-00008" : degre_perte,
    "ACC-000000-0000b" : classe,
    "ACC-000000-0000c" : marque,
    "ACC-000000-0000d" : telecommande,
    "ACC-000000-0000e" : bluetooth,
    "ACC-000000-0000f" : multiprogramme,
    "ACC-000000-0000g" : reglage_volume,
    "ACC-000000-0000h" : prothese_auditive_rechargeable,
    "ACC-000000-0000i" : microphone,
    "ACC-000000-0000j" : modele_piles,
    "ACC-000000-0000k" : systeme_anti_acouphenes,
    #"ACC-000000-0000l" : "Site Fabriquant",
    "ACC-000000-0000m" : precision_canaux,
    "ACC-000000-0000n" : synchro_binaurale,
    #"ACC-000000-0000o" : "Liens vidéo",
    #"ACC-000000-0000p" : "Partager ce site avec vos amis",
    "ACC-000000-0000q" : date_sortie,
}

