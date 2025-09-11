-- Migration script for QR codes data - Part 1
-- Execute this script AFTER running the main migration script
-- Use this script on the IAMC database (Microsoft SQL Server)

-- Insert QR codes data
SET IDENTITY_INSERT qr_codes ON;

-- QR codes data batch
IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '102')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (238, '102', 'Helder Rangel Leite', 'C:\Users\maikel.GTS\Pictures\Salida\qr_102.png', 'eb8c62aa2e0e61245f20e3abade62af3e716eee31cd4d95e128852c235670d76');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '107')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (239, '107', 'Andre Cabaia Eduardo', 'C:\Users\maikel.GTS\Pictures\Salida\qr_107.png', 'ef33da9f921cab6859c87a87a96b61863df18f398fb9d1e24d2fcd7727860bda');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '109')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (240, '109', 'Claudia Patricia Sequeira de Andrade', 'C:\Users\maikel.GTS\Pictures\Salida\qr_109.png', '6b05b7e172e298d039b006d46f5766115d4fb8e8de97ba733d4a71efe51e3c92');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '106')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (241, '106', 'Nauria de Fatima Cordeiro Escorcio', 'C:\Users\maikel.GTS\Pictures\Salida\qr_106.png', '34e201e96d3d0975dbaaebc804353228390cd75b5dfa5169648459c507b0b6f5');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '111')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (242, '111', 'Elizangela Patricia Silvestre Paulino', 'C:\Users\maikel.GTS\Pictures\Salida\qr_111.png', '99d585a71335e0322f47cdeb2720af82de9a1c2d14a74e62646cb97cc64d8ba9');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '11')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (243, '11', 'Ndemofiapo Nasser Augusto', 'C:\Users\maikel.GTS\Pictures\Salida\qr_11.png', '823636cfb6a72b1872f72b6ae1d2acdc3771b407a0b28a05d693708ba8b36e89');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '113')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (244, '113', 'Isabel Evalinda Pires Kamosso Garcia', 'C:\Users\maikel.GTS\Pictures\Salida\qr_113.png', '36b923ee0ee1e842c26b4352faca1d432fe729cedda6a5060b1c19927a282a5b');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '114')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (245, '114', 'Armando Nikolay Leitao Rodrigues', 'C:\Users\maikel.GTS\Pictures\Salida\qr_114.png', 'd24d5e6c69e1dab856481c8143141d17837f738f2376f78f0015ee67e69f3e33');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '118')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (246, '118', 'Manuel Antonio Paulo da Costa', 'C:\Users\maikel.GTS\Pictures\Salida\qr_118.png', '283d38c321b11117671fd311930a337d1abf2d28375c857ee2f24506b819fbdd');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '119')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (247, '119', 'Pedrito Joao Sozinho', 'C:\Users\maikel.GTS\Pictures\Salida\qr_119.png', '80601e5c5501e28ccd8302750bc7a69a0c9ec5b5b169e6e51e1b14fe67f1ea1b');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '120')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (248, '120', 'Antonio Francisco Baptista', 'C:\Users\maikel.GTS\Pictures\Salida\qr_120.png', 'ae7c85826fdca3f9327bf56f0513b87f63fbe32b0881e30d0be42e279e66ae48');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '122')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (249, '122', 'Miguel Joao Manuel Filho', 'C:\Users\maikel.GTS\Pictures\Salida\qr_122.png', '2e2accbabd9a320d27f37e2289afd9ac3b7009ef64755adf7a940ecde1564642');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '125')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (250, '125', 'Paulo Carlos da Silva Noy', 'C:\Users\maikel.GTS\Pictures\Salida\qr_125.png', '143a3585f5f7c89d0e8cbbcbadd168c00a1af5c8b21745a3f12fbea68d5e3d23');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '128')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (251, '128', 'Antonio Andre Chivanga Barros', 'C:\Users\maikel.GTS\Pictures\Salida\qr_128.png', '16596b82f8851b73baebd020737c3183f5e279f9f334776e5ea9400a10b9c7da');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '13')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (252, '13', 'Jose Joao Gaspar', 'C:\Users\maikel.GTS\Pictures\Salida\qr_13.png', '8d4680314edf04c4b40b4fba2b8eae22deef587d2081cf2a950ab7ed9ed6f9bf');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '132')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (253, '132', 'Joao Honore Luzolo', 'C:\Users\maikel.GTS\Pictures\Salida\qr_132.png', '600433abb0f339ffc5192434807a22bc70cb6fa8beb5ef30421bcf922a95251e');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '133')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (254, '133', 'Diego Rafael Custodio Neto', 'C:\Users\maikel.GTS\Pictures\Salida\qr_133.png', 'd51aebdacd690e5891ff86aef298a1fe1ad633d4953c86cc671a911e112946d2');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '227')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (255, '227', 'Nadio Bruno Manuel Gomes Fortunato', 'C:\Users\maikel.GTS\Pictures\Salida\qr_227.png', 'd8e2d9425fb1ddf90d8be2d919d869313d3b63585e6650e5eb33c2f669e7c76a');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '43')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (256, '43', 'Danilson Jose Maria Carvalho da Silva', 'C:\Users\maikel.GTS\Pictures\Salida\qr_43.png', '67bb78febe6381f5fd648b2a7879f900d8b5459006f718fdf22a4138dc002b23');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '5000011')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (257, '5000011', 'DTI 2', 'C:\Users\maikel.GTS\Pictures\Salida\qr_5000011.png', 'e9ed60786ce6174270b6bd106e264acb1c9f6a1185c1e1f500896721a55461dd');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '5000012')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (258, '5000012', 'DTI 3', 'C:\Users\maikel.GTS\Pictures\Salida\qr_5000012.png', '840cb3d9884daab62ecbc18527f609c80ba8aeb67cc34997e4279dd791cd0a3f');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '5000013')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (259, '5000013', 'DTI 4', 'C:\Users\maikel.GTS\Pictures\Salida\qr_5000013.png', 'a509c896958cf592073cc22fa4644b7b8548880d6f72efcbbb0c3bc55d0704ac');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '5000018')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (260, '5000018', 'Maikel Cuao', 'C:\Users\maikel.GTS\Pictures\Salida\qr_5000018.png', '90c251c74b9f0d8ba502a6ae7cc97943a0ba36fdb8cee44e34ce936afae0ff89');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '5000030')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (261, '5000030', 'Mavinga Fernandes', 'C:\Users\maikel.GTS\Pictures\Salida\qr_5000030.png', '9b2b75950aadf2a3f05a7ea2ecab522d042e1bdd8b4410e5e673fe0ab3990395');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '500005')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (262, '500005', 'DTI 1', 'C:\Users\maikel.GTS\Pictures\Salida\qr_500005.png', '6fb1fb5b0447304c4730c81eea4d503d8bbe552c33a3ea043fc36ca2ae32dc1f');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '5000054')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (263, '5000054', 'DTI 5', 'C:\Users\maikel.GTS\Pictures\Salida\qr_5000054.png', '8f5cafd0e6a27c904297f082be2859e8e1753b6e52f581bbf91b2222fec7e306');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '5000055')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (264, '5000055', 'DTI 6', 'C:\Users\maikel.GTS\Pictures\Salida\qr_5000055.png', 'abeae50288edaf49897f42c3b01e0ba0b7dbb81b678bc7dce06af723e2541167');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '74')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (265, '74', 'Maria do Ceu de Oliveira Garrido', 'C:\Users\maikel.GTS\Pictures\Salida\qr_74.png', '2c163022fa9eca29668dcdcd1e4b60cca6fdfaba813f5ec3a77dede24dc109de');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '130')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (266, '130', 'Frayma Amaro Sanchez', 'C:\Users\maikel.GTS\Pictures\Salida\qr_130.png', 'c527ffc613edbbabf2d933574e5705d51259010ba4f1c0ed865b6f3eff2394de');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '131')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (267, '131', 'Lisandro Angel Diaz Bisset', 'C:\Users\maikel.GTS\Pictures\Salida\qr_131.png', 'eb948488166d05981c8cf2d7a17d3d05bd0bf0fa5d399735eb2dfeea0d2469a7');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '134')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (268, '134', 'Delfina Ilda da Gama Ferreira', 'C:\Users\maikel.GTS\Pictures\Salida\qr_134.png', 'c3fcd9df5296c1997945934f6d7f36ed8879ddfac7b3384c96784a65002ef400');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '135')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (269, '135', 'Victoria Ndapona Goncalves Miguel Ruas', 'C:\Users\maikel.GTS\Pictures\Salida\qr_135.png', 'ea60c683cf061c10a05734bae0579d8f441976c130d9eea76901fff200378898');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '136')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (270, '136', 'Laciete Pereira da Conceicao Neto', 'C:\Users\maikel.GTS\Pictures\Salida\qr_136.png', '719ac8c20c9e36b379bc8597c5bc34ee61e75a0df7a445ff73087e89e6d5963d');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '137')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (271, '137', 'Rosa Rodrigues Neto Fernandes da Silva', 'C:\Users\maikel.GTS\Pictures\Salida\qr_137.png', 'fcc9f9090ee07f1b821f84adce1bab7f20c0afbd71a2e80fc64af2690974e57e');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '138')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (272, '138', 'Antonio Chimuco  Calei', 'C:\Users\maikel.GTS\Pictures\Salida\qr_138.png', '038833685e7ab9f76a4e9603fe7d47f71176a4ff04170473b35045f12f9ac313');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '139')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (273, '139', 'Amilcar Teodoro Pacheco', 'C:\Users\maikel.GTS\Pictures\Salida\qr_139.png', '7c6984fc9752bf76c4f4a3df31cd8ebdce8ea2d7c12e93d4b0738ce9303f3ad9');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '140')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (274, '140', 'Theophile Madikani Wadigesila', 'C:\Users\maikel.GTS\Pictures\Salida\qr_140.png', '9ab7faa0f564ce59957432b50c2d21cbd79a7e996e928b1f2488c89810ebb28b');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '14002')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (275, '14002', 'Rita Sebastiao Barbas Dala', 'C:\Users\maikel.GTS\Pictures\Salida\qr_14002.png', '07cf29d52ea3b7e10ed28041e4340b216e01af7e572d337cb03eec55b4e8af59');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '14005')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (276, '14005', 'Romeu Francisco Vicente Paulo', 'C:\Users\maikel.GTS\Pictures\Salida\qr_14005.png', 'b869cda6830b895157ac02b1ea3f5f4d9520d274caffeb8b0533f2a09ae0c8e4');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '14007')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (277, '14007', 'Tchissola Maria Coimbra ', 'C:\Users\maikel.GTS\Pictures\Salida\qr_14007.png', '77d8c7cb3c4fc8a09bc13f6e7de68848f73712661cd092635555f0f55fbed8c5');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '14008')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (278, '14008', 'Inacio Jose Evambi', 'C:\Users\maikel.GTS\Pictures\Salida\qr_14008.png', '210f2ca31dbd8ab3eb5a25d292394612bcde93e740b820f49b3d6af0c7da8240');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '14009')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (279, '14009', 'Nilcia Cleide da Silva Comboi', 'C:\Users\maikel.GTS\Pictures\Salida\qr_14009.png', '9f0b052298302204f8b4adcbd7fa7a2535ecb9fca8b2a2cb75d8607d9a20ca71');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '14014')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (280, '14014', 'Anito Kazumbula Pedro Pereira', 'C:\Users\maikel.GTS\Pictures\Salida\qr_14014.png', '024c6e9cd1f175171e9b5eb9b4a9155e41f9b0bf4d205a1aeb4bee95156cfeb6');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '14015')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (281, '14015', 'Ruth Situkuli Artur Lukamba Francisco', 'C:\Users\maikel.GTS\Pictures\Salida\qr_14015.png', '6e643fea515e1668b98f03c29a05f72816823ab0e9a315fb1d543e384421fbc5');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '14020')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (282, '14020', 'Vezua Antonia Mpovo Seke', 'C:\Users\maikel.GTS\Pictures\Salida\qr_14020.png', 'aab4e4bd27db0b14f8b0b195455b950159cf78dd04ee355381805acc38f958b7');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '142')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (283, '142', 'Jose Zua Lucas Augusto', 'C:\Users\maikel.GTS\Pictures\Salida\qr_142.png', 'f7cbfa2ff095de7a97c0859124036bd3df0f53474cb34e763f36be7c3524adeb');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '148')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (284, '148', 'Danilson Bartolomeu Pereira da Conceicao', 'C:\Users\maikel.GTS\Pictures\Salida\qr_148.png', '3de27677a42f9a589fde510c59d85faacb166360cc511527e7c7db916b205b7e');

IF NOT EXISTS (SELECT 1 FROM qr_codes WHERE contact_id = '15')
    INSERT INTO qr_codes (id, contact_id, nombre, archivo_qr, firma) VALUES (285, '15', 'Lilhan de Souza Ferro Barbosa', 'C:\Users\maikel.GTS\Pictures\Salida\qr_15.png', '170c70bfb2d94f7b947c0fca476322f0415fc371cfaf0321e541985cb813c9ea');

SET IDENTITY_INSERT qr_codes OFF;

-- Reseed qr_codes identity to continue from the next available ID
DECLARE @max_qr_id INT;
SELECT @max_qr_id = ISNULL(MAX(id), 0) FROM qr_codes;
DBCC CHECKIDENT ('qr_codes', RESEED, @max_qr_id);

-- Verification query
SELECT COUNT(*) as 'Total QR Codes Inserted' FROM qr_codes;

PRINT 'QR codes migration Part 1 completed successfully!';
PRINT 'NOTE: This script includes the first batch of QR code records.';
PRINT 'The full dataset contains more records. Create additional migration scripts for remaining data if needed.';
