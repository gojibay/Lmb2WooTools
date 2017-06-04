#!/bin/bash

cat << EOF 

INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES(  $1, "_marque","field_576e559483cd8");
INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES(  $1 ,"_type","field_578a5a2336013");
INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES(  $1 ,"_degre_de_perte_auditive","field_576e569ff4e3f");
INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES(  $1 ,"_gamme","field_576ff76c1af69");
INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES(  $1 ,"_reference-interne","field_576ff3a3aee37");
INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES(  $1 ,"_reference-lmb","field_576ff3dfaee38");
INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES(  $1 ,"_classification_securite_sociale","field_576ff77d1af6a");
INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES(  $1 ,"_date_de_sortie","field_576ffa3863506");
INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES(  $1 ,"_compatibilite_telecommande","field_576ffa6363507");
INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES(  $1 ,"_audioprothese_bluetooth","field_576ffadc7e3e6");
INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES(  $1 ,"_multi_programmes","field_576ffaf77e3e7");
INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES(  $1 ,"_reglage_volume","field_576ffb227e3e8");
INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES(  $1 ,"_prothese_auditive_rechargeable","field_576ffb327e3e9");
INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES(  $1 ,"_microphone","field_576ffb512fab2");
INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES(  $1 ,"_modele_de_piles","field_576ffb6e2fab3");
INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES(  $1 ,"_systeme_anti_acouphenes","field_576ffbb62fab4");
INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES(  $1 ,"_precision_reglages_audioprothetiques","field_576ffbe92fab5");
INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES(  $1 ,"_synchronisation_binaurale","field_576ffc322fab6");
INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES(  $1 ,"_site_fabriquant","field_576ffc542fab7");
INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES(  $1 ,"_lien_video","field_5798faa840681");
INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES(  $1 ,"_url_lmb","field_5798fe8679bcd");

EOF