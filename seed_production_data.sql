-- ========================================================
-- PRODUCTION SIMULATION SEED SCRIPT (Tunisia Context)
-- Generates: 24 Regions, 50+ Delegations, 10+ Schools,
-- and exactly 200 Users (1 Admin, 30 Inspectors, 169 Teachers)
-- with completely correct schemas and realistic Tunisian data.
-- All generated IDs start from 10 (or above) to preserve
-- your existing database records (IDs 1-9).
-- ========================================================

SET FOREIGN_KEY_CHECKS = 0;

-- Safe Cleanup: Only delete simulation data starting at ID 10+
-- This keeps your manually created data (IDs 1-9) completely untouched!
DELETE FROM `action_logs` WHERE `user_id` >= 10;
DELETE FROM `notifications` WHERE `recipient_id` >= 10;
DELETE FROM `messages` WHERE `sender_id` >= 10;
DELETE FROM `conversations` WHERE `user1_id` >= 10 OR `user2_id` >= 10;
DELETE FROM `activity_guests` WHERE `guest_user_id` >= 10;
DELETE FROM `activity_reports` WHERE `id` >= 10;
DELETE FROM `activities` WHERE `id` >= 10;
DELETE FROM `quiz_submissions` WHERE `id` >= 10;
DELETE FROM `quiz_questions` WHERE `id` >= 10;
DELETE FROM `quiz_assignments` WHERE `id` >= 10;
DELETE FROM `quizzes` WHERE `id` >= 10;
DELETE FROM `course_assignments` WHERE `id` >= 10;
DELETE FROM `course_lessons` WHERE `id` >= 10;
DELETE FROM `course_modules` WHERE `id` >= 10;
DELETE FROM `courses` WHERE `id` >= 10;
DELETE FROM `teacher_profiles` WHERE `id` >= 10;
DELETE FROM `inspector_profiles` WHERE `id` >= 10;
DELETE FROM `etablissements` WHERE `id` >= 10;
DELETE FROM `dependencies` WHERE `id` >= 10;
DELETE FROM `departments` WHERE `id` >= 10;
DELETE FROM `delegations` WHERE `id` >= 10;
DELETE FROM `regions` WHERE `id` >= 10;
DELETE FROM `users` WHERE `id` >= 10;

-- 1. SEED REGIONS (The 24 Governorates of Tunisia starting at ID 10)
INSERT INTO `regions` (`id`, `name`) VALUES
(10, 'Tunis'), (11, 'Ariana'), (12, 'Ben Arous'), (13, 'Manouba'), (14, 'Nabeul'), (15, 'Zaghouan'),
(16, 'Bizerte'), (17, 'Béja'), (18, 'Jendouba'), (19, 'Le Kef'), (20, 'Siliana'), (21, 'Sousse'),
(22, 'Monastir'), (23, 'Mahdia'), (24, 'Sfax'), (25, 'Kairouan'), (26, 'Kasserine'), (27, 'Sidi Bouzid'),
(28, 'Gabès'), (29, 'Medenine'), (30, 'Tataouine'), (31, 'Gafsa'), (32, 'Tozeur'), (33, 'Kebili');

-- 2. SEED DELEGATIONS (52 delegations starting at ID 10, mapping to correct regions)
INSERT INTO `delegations` (`id`, `name`, `region_id`) VALUES
-- Tunis (Delegations 10-19, region 10)
(10, 'Tunis Medina', 10), (11, 'Sidi El Béchir', 10), (12, 'La Marsa', 10), (13, 'Le Bardo', 10), (14, 'Carthage', 10),
(15, 'El Omrane', 10), (16, 'El Menzah', 10), (17, 'Hay El Khadra', 10), (18, 'La Goulette', 10), (19, 'Sidi Hassine', 10),
-- Ariana (Delegations 20-25, region 11)
(20, 'Ariana Ville', 11), (21, 'La Soukra', 11), (22, 'Raoued', 11), (23, 'Kalâat el-Andalous', 11), (24, 'Sidi Thabet', 11), (25, 'Mnihla', 11),
-- Ben Arous (Delegations 26-31, region 12)
(26, 'Ben Arous Ville', 12), (27, 'Megrine', 12), (28, 'Radès', 12), (29, 'Hammam Lif', 12), (30, 'Bou Mhel el-Bassatine', 12), (31, 'Ezzahra', 12),
-- Nabeul (Delegations 32-39, region 14)
(32, 'Nabeul Ville', 14), (33, 'Hammamet', 14), (34, 'Korba', 14), (35, 'Menzel Temime', 14), (36, 'Kelibia', 14), (37, 'Soliman', 14), (38, 'Grombalia', 14), (39, 'Dar Châabane El Fehri', 14),
-- Sousse (Delegations 40-47, region 21)
(40, 'Sousse Medina', 21), (41, 'Sousse Riadh', 21), (42, 'Akouda', 21), (43, 'Hammam Sousse', 21), (44, 'Kalaâ Kebira', 21), (45, 'Kalaâ Seghira', 21), (46, 'Msaken', 21), (47, 'Sousse Jaouhara', 21),
-- Monastir (Delegations 48-53, region 22)
(48, 'Monastir Ville', 22), (49, 'Moknine', 22), (50, 'Jemmal', 22), (51, 'Ksar Hellal', 22), (52, 'Téboulba', 22), (53, 'Bekalta', 22),
-- Sfax (Delegations 54-61, region 24)
(54, 'Sfax Ville', 24), (55, 'Sfax Ouest', 24), (56, 'Sakiet Ezzit', 24), (57, 'Sakiet Eddaier', 24), (58, 'Sfax Sud', 24), (59, 'Thyna', 24), (60, 'El Hencha', 24), (61, 'Jebeniana', 24);

-- 3. SEED DEPARTMENTS (Starting at ID 10)
INSERT INTO `departments` (`id`, `name`, `delegation_id`) VALUES
(10, 'Direction Régionale Tunis 1', 10),
(11, 'Direction Régionale Sousse', 40),
(12, 'Direction Régionale Sfax', 54);

-- 4. SEED DEPENDENCIES (Starting at ID 10)
INSERT INTO `dependencies` (`id`, `name`, `delegation_id`) VALUES
(10, 'Circonscription Tunis 1', 10),
(11, 'Circonscription Sousse Nord', 40),
(12, 'Circonscription Sfax Est', 54);

-- 5. SEED ETABLISSEMENTS (Schools starting at ID 10)
INSERT INTO `etablissements` (`id`, `name`, `school_level`, `dependency_id`) VALUES
(10, 'Lycée Pilote Tunis', 'SECONDARY', 10),
(11, 'Lycée Rue du Pacha', 'SECONDARY', 10),
(12, 'Collège Sadiki', 'PREPARATORY', 10),
(13, 'Lycée Pilote Sousse', 'SECONDARY', 11),
(14, 'Lycée Tahar Sfar Sousse', 'SECONDARY', 11),
(15, 'Lycée Pilote Sfax', 'SECONDARY', 12),
(16, 'Collège Majida Boulila', 'PREPARATORY', 12),
(17, 'Lycée Carthage Presidence', 'SECONDARY', 10),
(18, 'Lycée Ibn Charaf Tunis', 'SECONDARY', 10),
(19, 'Collège Pilote Les Berges du Lac', 'PREPARATORY', 10);

-- 6. SEED USERS (Exactly 200 Users)
-- We use: 1 Admin, 30 Inspectors, 169 Teachers.
-- Password for all is 'password' -> $2a$10$8.UnVuG9HHgffUDAlk8qfOuVGkqRzgVymGe07xd00DMxs.TVu4ATA

-- 6.1 Admin (1 User)
INSERT INTO `users` (`id`, `enabled`, `is_microsoft_connected`, `profile_completed`, `created_at`, `serial_code`, `email`, `password`, `role`) VALUES
(10, b'1', b'0', b'1', NOW(), 'ADMIN-010', 'admin.system@inspector.tn', '$2a$10$8.UnVuG9HHgffUDAlk8qfOuVGkqRzgVymGe07xd00DMxs.TVu4ATA', 'ADMIN');

-- 6.2 Inspectors (30 Users: IDs 101 to 130)
-- 10 Manual Inspectors
INSERT INTO `users` (`id`, `enabled`, `is_microsoft_connected`, `profile_completed`, `created_at`, `serial_code`, `email`, `password`, `role`) VALUES
(101, b'1', b'0', b'1', NOW(), 'I-101', 'mohamed.ali@inspector.tn', '$2a$10$8.UnVuG9HHgffUDAlk8qfOuVGkqRzgVymGe07xd00DMxs.TVu4ATA', 'INSPECTOR'),
(102, b'1', b'0', b'1', NOW(), 'I-102', 'ahmed.benali@inspector.tn', '$2a$10$8.UnVuG9HHgffUDAlk8qfOuVGkqRzgVymGe07xd00DMxs.TVu4ATA', 'INSPECTOR'),
(103, b'1', b'0', b'1', NOW(), 'I-103', 'fatma.mansour@inspector.tn', '$2a$10$8.UnVuG9HHgffUDAlk8qfOuVGkqRzgVymGe07xd00DMxs.TVu4ATA', 'INSPECTOR'),
(104, b'1', b'0', b'1', NOW(), 'I-104', 'yassine.trabelsi@inspector.tn', '$2a$10$8.UnVuG9HHgffUDAlk8qfOuVGkqRzgVymGe07xd00DMxs.TVu4ATA', 'INSPECTOR'),
(105, b'1', b'0', b'1', NOW(), 'I-105', 'leila.mejri@inspector.tn', '$2a$10$8.UnVuG9HHgffUDAlk8qfOuVGkqRzgVymGe07xd00DMxs.TVu4ATA', 'INSPECTOR'),
(106, b'1', b'0', b'1', NOW(), 'I-106', 'sami.hamdi@inspector.tn', '$2a$10$8.UnVuG9HHgffUDAlk8qfOuVGkqRzgVymGe07xd00DMxs.TVu4ATA', 'INSPECTOR'),
(107, b'1', b'0', b'1', NOW(), 'I-107', 'rym.gharbi@inspector.tn', '$2a$10$8.UnVuG9HHgffUDAlk8qfOuVGkqRzgVymGe07xd00DMxs.TVu4ATA', 'INSPECTOR'),
(108, b'1', b'0', b'1', NOW(), 'I-108', 'mourad.jouini@inspector.tn', '$2a$10$8.UnVuG9HHgffUDAlk8qfOuVGkqRzgVymGe07xd00DMxs.TVu4ATA', 'INSPECTOR'),
(109, b'1', b'0', b'1', NOW(), 'I-109', 'ines.belhadj@inspector.tn', '$2a$10$8.UnVuG9HHgffUDAlk8qfOuVGkqRzgVymGe07xd00DMxs.TVu4ATA', 'INSPECTOR'),
(110, b'1', b'0', b'1', NOW(), 'I-110', 'khalil.amri@inspector.tn', '$2a$10$8.UnVuG9HHgffUDAlk8qfOuVGkqRzgVymGe07xd00DMxs.TVu4ATA', 'INSPECTOR');

-- 20 Dynamic Inspectors
INSERT INTO `users` (`id`, `enabled`, `is_microsoft_connected`, `profile_completed`, `created_at`, `serial_code`, `email`, `password`, `role`)
SELECT 110 + id, b'1', b'0', b'1', NOW(), CONCAT('I-', 110 + id), CONCAT('inspector.', id, '@inspector.tn'), '$2a$10$8.UnVuG9HHgffUDAlk8qfOuVGkqRzgVymGe07xd00DMxs.TVu4ATA', 'INSPECTOR'
FROM (
    SELECT 1 AS id UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION 
    SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10 UNION 
    SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 UNION SELECT 15 UNION 
    SELECT 16 UNION SELECT 17 UNION SELECT 18 UNION SELECT 19 UNION SELECT 20
) AS t;

-- 6.3 Teachers (169 Users: IDs 200 to 368)
INSERT INTO `users` (`id`, `enabled`, `is_microsoft_connected`, `profile_completed`, `created_at`, `serial_code`, `email`, `password`, `role`)
SELECT 200 + id, b'1', b'0', b'1', NOW(), CONCAT('T-', 200 + id), CONCAT('teacher.', id, '@edu.tn'), '$2a$10$8.UnVuG9HHgffUDAlk8qfOuVGkqRzgVymGe07xd00DMxs.TVu4ATA', 'TEACHER'
FROM (
    SELECT a.i + b.i * 10 + c.i * 100 AS id
    FROM (SELECT 0 AS i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) a
    CROSS JOIN (SELECT 0 AS i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) b
    CROSS JOIN (SELECT 0 AS i UNION SELECT 1) c
) AS t
WHERE id < 169;


-- 7. SEED INSPECTOR PROFILES (30 Profiles: user_ids 101 to 130)
-- 5 Manual Inspector Profiles
INSERT INTO `inspector_profiles` (`id`, `user_id`, `first_name`, `last_name`, `phone`, `language`, `rank`, `school_level`, `subject`) VALUES
(10, 101, 'Mohamed', 'Ali', '+21698123456', 'ARABIC', 'INSPECTOR_GENERAL', 'SECONDARY', 'MATH'),
(11, 102, 'Ahmed', 'Ben Ali', '+21698765432', 'ARABIC', 'INSPECTOR_PRINCIPAL', 'SECONDARY', 'PHYSICS'),
(12, 103, 'Fatma', 'Mansour', '+21697111222', 'FRENCH', 'INSPECTOR', 'PREPARATORY', 'FRENCH'),
(13, 104, 'Yassine', 'Trabelsi', '+21695444555', 'ARABIC', 'INSPECTOR_REGIONAL', 'PRIMARY', 'ARABIC'),
(14, 105, 'Leila', 'Mejri', '+21622333444', 'FRENCH', 'INSPECTOR', 'SECONDARY', 'COMPUTER_SCIENCE');

-- 25 Dynamic Inspector Profiles
INSERT INTO `inspector_profiles` (`user_id`, `first_name`, `last_name`, `phone`, `language`, `rank`, `school_level`, `subject`)
SELECT 
    id, 
    ELT(1 + FLOOR(RAND() * 10), 'Hichem', 'Moncef', 'Kamel', 'Slim', 'Tarek', 'Wajdi', 'Nabil', 'Mourad', 'Habib', 'Anis'),
    ELT(1 + FLOOR(RAND() * 10), 'Hammami', 'Trabelsi', 'Gharbi', 'Riahi', 'Jaziri', 'Khlifi', 'Saidi', 'Chebbi', 'Dridi', 'Louati'),
    CONCAT('+216', FLOOR(RAND() * 89999999 + 10000000)),
    ELT(1 + FLOOR(RAND() * 3), 'English', 'French', 'Arabic'),
    ELT(1 + FLOOR(RAND() * 5), 'INSPECTOR', 'INSPECTOR_PRINCIPAL', 'INSPECTOR_GENERAL', 'INSPECTOR_GENERAL_ADJOINT', 'INSPECTOR_REGIONAL'),
    ELT(1 + FLOOR(RAND() * 3), 'PRIMARY', 'PREPARATORY', 'SECONDARY'),
    ELT(1 + FLOOR(RAND() * 15), 'ARABIC','FRENCH','ENGLISH','MATH','PHYSICS','CHEMISTRY','BIOLOGY','HISTORY_GEOGRAPHY','PHILOSOPHY','ISLAMIC_STUDIES','PHYSICAL_EDUCATION','COMPUTER_SCIENCE','ECONOMICS','ARTS','MUSIC')
FROM `users` 
WHERE role = 'INSPECTOR' AND id NOT IN (101, 102, 103, 104, 105);


-- 8. SEED TEACHER PROFILES (169 Profiles: user_ids 200 to 368)
-- 5 Manual Teacher Profiles
INSERT INTO `teacher_profiles` (`id`, `user_id`, `first_name`, `last_name`, `phone`, `subject`, `language`, `delegation_id`, `dependency_id`, `etablissement_id`) VALUES
(100, 200, 'Sami', 'Hamdi', '+21620000001', 'MATH', 'French', 10, 10, 10),
(101, 201, 'Amel', 'Gharbi', '+21620000002', 'MATH', 'English', 10, 10, 11),
(102, 202, 'Hedi', 'Dridi', '+21620000003', 'PHYSICS', 'French', 40, 11, 13),
(103, 203, 'Zohra', 'Ben Salha', '+21620000004', 'FRENCH', 'French', 40, 11, 14),
(104, 204, 'Walid', 'Jaziri', '+21620000005', 'COMPUTER_SCIENCE', 'English', 54, 12, 15);

-- 164 Dynamic Teacher Profiles
INSERT INTO `teacher_profiles` (`user_id`, `first_name`, `last_name`, `phone`, `subject`, `language`, `delegation_id`, `dependency_id`, `etablissement_id`)
SELECT 
    id, 
    ELT(1 + FLOOR(RAND() * 10), 'Abderrahmane', 'Bassem', 'Chokri', 'Dhia', 'Elyes', 'Fares', 'Ghaith', 'Habib', 'Imed', 'Jalel'),
    ELT(1 + FLOOR(RAND() * 10), 'Abidi', 'Baccouche', 'Chaibi', 'Dahmani', 'Elloumi', 'Farhat', 'Guizani', 'Hadhri', 'Idoudi', 'Jebali'),
    CONCAT('+216', FLOOR(RAND() * 89999999 + 10000000)),
    ELT(1 + FLOOR(RAND() * 15), 'ARABIC','FRENCH','ENGLISH','MATH','PHYSICS','CHEMISTRY','BIOLOGY','HISTORY_GEOGRAPHY','PHILOSOPHY','ISLAMIC_STUDIES','PHYSICAL_EDUCATION','COMPUTER_SCIENCE','ECONOMICS','ARTS','MUSIC'),
    ELT(1 + FLOOR(RAND() * 3), 'English', 'French', 'Arabic'),
    10 + FLOOR(RAND() * 52), -- delegation_id from 10 to 61
    10 + FLOOR(RAND() * 3),  -- dependency_id from 10 to 12
    10 + FLOOR(RAND() * 10)  -- etablissement_id from 10 to 19
FROM `users` 
WHERE role = 'TEACHER' AND id NOT IN (200, 201, 202, 203, 204);


-- 9. SEED ACTION LOGS (Simulate recent production activity logs)
INSERT INTO `action_logs` (`action_type`, `created_at`, `description`, `entity_type`, `user_id`, `ip_address`)
SELECT 
    'LOGIN', 
    DATE_SUB(NOW(), INTERVAL (RAND() * 1000) MINUTE), 
    'User logged in from production simulation', 
    'User', 
    id, 
    CONCAT('197.1.', FLOOR(RAND()*255), '.', FLOOR(RAND()*255))
FROM `users` 
LIMIT 120;


-- 10. SEED NOTIFICATIONS (Simulate pending notifications)
INSERT INTO `notifications` (`is_read`, `created_at`, `recipient_id`, `type`, `title`, `message`)
SELECT 
    0, 
    NOW(), 
    id, 
    'SYSTEM', 
    'Production Simulation Initialized', 
    'Your account is successfully synced with 200 Tunisian users.'
FROM `users`
WHERE role IN ('INSPECTOR', 'TEACHER');

SET FOREIGN_KEY_CHECKS = 1;
COMMIT;
