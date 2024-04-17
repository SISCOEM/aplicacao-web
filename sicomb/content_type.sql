/*
 SQL PARA RESOLVER ERRO DE CRIAÇÃO DA TABELA CONTENT TYPE
*/

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

INSERT INTO sicomb.django_content_type (app_label,model) VALUES
	 ('admin','logentry'),
	 ('auth','group'),
	 ('auth','permission'),
	 ('contenttypes','contenttype'),
	 ('equipment','bullet'),
	 ('equipment','equipment'),
	 ('equipment','model_accessory'),
	 ('equipment','model_armament'),
	 ('equipment','model_grenada'),
	 ('equipment','model_wearable');
INSERT INTO sicomb.django_content_type (app_label,model) VALUES
	 ('load','equipment_load'),
	 ('load','load'),
	 ('police','police'),
	 ('sessions','session');