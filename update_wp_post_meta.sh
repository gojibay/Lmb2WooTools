#!/bin/bash

cat << EOF 


UPDATE wp_postmeta SET meta_value = "field_576e559483cd8" WHERE post_id = $1 AND meta_key =  "_marque";
UPDATE wp_postmeta SET meta_value = "field_578a5a2336013" WHERE post_id = $1 AND meta_key =  "_type";
UPDATE wp_postmeta SET meta_value = "field_576e569ff4e3f" WHERE post_id = $1 AND meta_key =  "_degre_de_perte_auditive";
UPDATE wp_postmeta SET meta_value = "field_576ff76c1af69" WHERE post_id = $1 AND meta_key =  "_gamme";
UPDATE wp_postmeta SET meta_value = "field_576ff3a3aee37" WHERE post_id = $1 AND meta_key =  "_reference-interne";
UPDATE wp_postmeta SET meta_value = "field_576ff3dfaee38" WHERE post_id = $1 AND meta_key =  "_reference-lmb";
UPDATE wp_postmeta SET meta_value = "field_576ff77d1af6a" WHERE post_id = $1 AND meta_key =  "_classification_securite_sociale";
UPDATE wp_postmeta SET meta_value = "field_576ffa3863506" WHERE post_id = $1 AND meta_key =  "_date_de_sortie";
UPDATE wp_postmeta SET meta_value = "field_576ffa6363507" WHERE post_id = $1 AND meta_key =  "_compatibilite_telecommande";
UPDATE wp_postmeta SET meta_value = "field_576ffadc7e3e6" WHERE post_id = $1 AND meta_key =  "_audioprothese_bluetooth";
UPDATE wp_postmeta SET meta_value = "field_576ffaf77e3e7" WHERE post_id = $1 AND meta_key =  "_multi_programmes";
UPDATE wp_postmeta SET meta_value = "field_576ffb227e3e8" WHERE post_id = $1 AND meta_key =  "_reglage_volume";
UPDATE wp_postmeta SET meta_value = "field_576ffb327e3e9" WHERE post_id = $1 AND meta_key =  "_prothese_auditive_rechargeable";
UPDATE wp_postmeta SET meta_value = "field_576ffb512fab2" WHERE post_id = $1 AND meta_key =  "_microphone";
UPDATE wp_postmeta SET meta_value = "field_576ffb6e2fab3" WHERE post_id = $1 AND meta_key =  "_modele_de_piles";
UPDATE wp_postmeta SET meta_value = "field_576ffbb62fab4" WHERE post_id = $1 AND meta_key =  "_systeme_anti_acouphenes";
UPDATE wp_postmeta SET meta_value = "field_576ffbe92fab5" WHERE post_id = $1 AND meta_key =  "_precision_reglages_audioprothetiques";
UPDATE wp_postmeta SET meta_value = "field_576ffc322fab6" WHERE post_id = $1 AND meta_key =  "_synchronisation_binaurale";
UPDATE wp_postmeta SET meta_value = "field_576ffc542fab7" WHERE post_id = $1 AND meta_key =  "_site_fabriquant";
UPDATE wp_postmeta SET meta_value = "field_5798faa840681" WHERE post_id = $1 AND meta_key =  "_lien_video";
UPDATE wp_postmeta SET meta_value = "field_5798fe8679bcd" WHERE post_id = $1 AND meta_key =  "_url_lmb";




EOF


#IF EXISTS(SELECT * FROM wp_postmeta WHERE post_id = 5650 AND meta_key =  "_url_lmb") 
#THEN 
#UPDATE wp_postmeta SET meta_value = "field_5798fe8679bcd" WHERE post_id = $1 AND meta_key =  "_url_lmb" 
#ELSE 
#INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES(  5650, "_url_lmb", "field_5798fe8679bcd");
