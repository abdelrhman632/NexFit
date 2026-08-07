INSERT INTO Products (
ProductName,
ProductBrand,
ProductModel,
ProductSKU,
ProductCategory,
ProductGender,
ProductPrice,
ProductMaterial,
ProductUsage,
ProductSurface,
ProductSupportType,
ProductCushioning,
ProductBreathability,
ProductWeight,
ProductWaterproof,
ProductDescription
)
VALUES
-- Nike
('Nike Revolution 7','Nike','Revolution 7','NK-REV7-001','Running','Men',3400,'Mesh','Daily Running','Road','Neutral','Medium','High',270,FALSE,'Affordable running shoe for beginners.'),
('Nike Downshifter 13','Nike','Downshifter 13','NK-DS13-001','Running','Women',3900,'Mesh','Walking','Road','Neutral','Medium','High',265,FALSE,'Comfortable walking and light running shoe.'),
('Nike Metcon 9','Nike','Metcon 9','NK-MTC9-001','Training','Unisex',7600,'Mesh','Gym','Indoor','Stability','Firm','Medium',350,FALSE,'Cross-training shoe for weightlifting and HIIT.'),
('Nike Court Vision Low','Nike','Court Vision Low','NK-CVL-001','Lifestyle','Men',4200,'Leather','Casual','Street','Neutral','Low','Low',360,FALSE,'Classic everyday sneaker inspired by basketball.'),
('Nike Air Force 1','Nike','Air Force 1','NK-AF1-001','Lifestyle','Unisex',6200,'Leather','Casual','Street','Neutral','Medium','Low',430,FALSE,'Iconic lifestyle sneaker.'),
-- Adidas
('Adidas Duramo SL','Adidas','Duramo SL','AD-DURSL-001','Running','Men',3600,'Mesh','Daily Running','Road','Neutral','Medium','High',280,FALSE,'Comfortable everyday running shoe.'),
('Adidas Runfalcon 5','Adidas','Runfalcon 5','AD-RF5-001','Running','Women',3300,'Mesh','Walking','Road','Neutral','Medium','High',275,FALSE,'Versatile running and walking shoe.'),
('Adidas Dropset Trainer','Adidas','Dropset Trainer','AD-DST-001','Training','Men',7100,'Mesh','Gym','Indoor','Stability','Firm','Medium',355,FALSE,'Stable gym training shoe.'),
('Adidas Grand Court','Adidas','Grand Court','AD-GC-001','Lifestyle','Unisex',4300,'Leather','Casual','Street','Neutral','Low','Low',395,FALSE,'Classic tennis-inspired sneaker.'),
('Adidas Terrex AX4','Adidas','Terrex AX4','AD-TRX4-001','Hiking','Men',7200,'Synthetic','Hiking','Trail','Stability','Medium','Medium',410,TRUE,'Lightweight hiking shoe.'),
-- ASICS
('ASICS GT-2000 13','ASICS','GT-2000 13','AS-GT13-001','Running','Men',8500,'Mesh','Daily Running','Road','Stability','High','High',290,FALSE,'Supportive running shoe for overpronators.'),
('ASICS Gel Venture 10','ASICS','Gel Venture 10','AS-GV10-001','Trail Running','Men',5800,'Mesh','Trail Running','Trail','Neutral','Medium','Medium',320,FALSE,'Trail running shoe for uneven terrain.'),
('ASICS Court FF 3','ASICS','Court FF 3','AS-CFF3-001','Tennis','Unisex',9600,'Mesh','Tennis','Court','Stability','Medium','High',340,FALSE,'Professional tennis shoe.'),
-- New Balance
('New Balance 574','New Balance','574','NB-574-001','Lifestyle','Unisex',5900,'Suede/Mesh','Casual','Street','Neutral','Medium','Medium',330,FALSE,'Classic lifestyle sneaker.'),
('New Balance Fresh Foam More v5','New Balance','More v5','NB-MORE5-001','Running','Men',8900,'Mesh','Long Distance','Road','Neutral','Maximum','High',305,FALSE,'Maximum cushioning running shoe.'),
('New Balance FuelCell Rebel v4','New Balance','Rebel v4','NB-RBL4-001','Running','Men',8400,'Mesh','Speed Training','Road','Neutral','Medium','High',220,FALSE,'Lightweight speed trainer.'),
-- HOKA
('HOKA Speedgoat 6','HOKA','Speedgoat 6','HK-SG6-001','Trail Running','Unisex',9800,'Mesh','Trail Running','Trail','Neutral','High','High',280,FALSE,'Premium trail running shoe.'),
('HOKA Transport','HOKA','Transport','HK-TRP-001','Walking','Unisex',8600,'Mesh','Walking','Road','Neutral','High','High',300,FALSE,'Comfort shoe for walking and commuting.'),
-- Brooks
('Brooks Adrenaline GTS 24','Brooks','Adrenaline GTS 24','BK-ADR24-001','Running','Men',8900,'Mesh','Daily Running','Road','Stability','High','High',295,FALSE,'Supportive running shoe.'),
('Brooks Beast GTS 24','Brooks','Beast GTS 24','BK-BST24-001','Walking','Men',9100,'Mesh','Walking','Road','Motion Control','Maximum','Medium',340,FALSE,'Maximum support walking shoe.'),
-- Puma
('Puma Velocity Nitro 3','Puma','Velocity Nitro 3','PM-VN3-001','Running','Men',6200,'Mesh','Daily Running','Road','Neutral','High','High',260,FALSE,'Responsive daily trainer.'),
('Puma Deviate Nitro Elite','Puma','Deviate Nitro Elite','PM-DNE-001','Running','Unisex',11500,'Mesh','Racing','Road','Neutral','High','High',210,FALSE,'Carbon-plated racing shoe.'),
('Puma Palermo','Puma','Palermo','PM-PLR-001','Lifestyle','Unisex',4800,'Suede','Casual','Street','Neutral','Low','Low',340,FALSE,'Retro casual sneaker.'),
-- Skechers
('Skechers GO WALK 7','Skechers','GO WALK 7','SK-GW7-001','Walking','Unisex',4600,'Mesh','Walking','Road','Neutral','High','High',250,FALSE,'Comfortable walking shoe.'),
('Skechers Arch Fit 2.0','Skechers','Arch Fit 2.0','SK-AF2-001','Walking','Men',5300,'Mesh','Standing All Day','Road','Arch Support','High','High',295,FALSE,'Excellent arch support for professionals.'),
('Skechers Uno','Skechers','Uno','SK-UNO-001','Lifestyle','Unisex',4100,'Synthetic','Casual','Street','Neutral','Medium','Medium',340,FALSE,'Lifestyle sneaker for everyday use.'),
-- Converse
('Converse Chuck Taylor High','Converse','Chuck Taylor High','CV-CTH-001','Lifestyle','Unisex',3500,'Canvas','Casual','Street','Neutral','Low','Medium',390,FALSE,'Classic canvas sneaker.'),
('Converse Run Star Motion','Converse','Run Star Motion','CV-RSM-001','Lifestyle','Unisex',6200,'Canvas','Fashion','Street','Neutral','Medium','Medium',420,FALSE,'Modern platform sneaker.'),
-- Vans
('Vans Old Skool','Vans','Old Skool','VN-OS-001','Lifestyle','Unisex',3900,'Canvas','Casual','Street','Neutral','Low','Medium',360,FALSE,'Classic skate-inspired sneaker.'),
('Vans UltraRange EXO','Vans','UltraRange EXO','VN-URX-001','Walking','Unisex',5600,'Mesh','Travel','Mixed','Neutral','Medium','High',310,FALSE,'Comfortable travel and walking shoe.'),
-- Under Armour
('UA Charged Assert 10','Under Armour','Charged Assert 10','UA-CA10-001','Running','Men',4700,'Mesh','Daily Running','Road','Neutral','Medium','High',285,FALSE,'Affordable everyday running shoe.'),
('UA TriBase Reign 6','Under Armour','TriBase Reign 6','UA-TBR6-001','Training','Unisex',7900,'Mesh','Gym','Indoor','Stability','Firm','Medium',360,FALSE,'High-performance cross-training shoe.'),
-- Salomon
('Salomon XT-6','Salomon','XT-6','SL-XT6-001','Trail Running','Unisex',11900,'Mesh','Trail Running','Trail','Neutral','High','High',365,FALSE,'Professional trail running shoe.'),
('Salomon X Ultra 5','Salomon','X Ultra 5','SL-XU5-001','Hiking','Men',11200,'Synthetic','Hiking','Trail','Stability','Medium','Medium',390,TRUE,'Water-resistant hiking shoe.'),
-- Mizuno
('Mizuno Wave Rider 28','Mizuno','Wave Rider 28','MZ-WR28-001','Running','Men',8700,'Mesh','Daily Running','Road','Neutral','High','High',280,FALSE,'Reliable neutral running shoe.');