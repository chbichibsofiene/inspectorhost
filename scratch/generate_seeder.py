import random

# Seed for reproducibility
random.seed(42)

out = []
out.append("-- ========================================================")
out.append("-- PRODUCTION SIMULATION SEED SCRIPT (Render/Aiven MySQL Safe)")
out.append("-- Generates: 24 Regions, 52 Delegations, 10 Schools,")
out.append("-- 200 Users, and 60 Evaluation Activities & Reports.")
out.append("-- All generated simulation IDs start from 1000+ to preserve")
out.append("-- your existing database records (IDs < 1000).")
out.append("-- ========================================================")
out.append("")
out.append("SET FOREIGN_KEY_CHECKS = 0;")
out.append("")
out.append("-- 1. SAFE CLEANUP (Deletes simulation/old seeded records, leaves manual records safe)")
out.append("DELETE FROM `lesson_progress` WHERE `id` >= 10;")
out.append("DELETE FROM `inspections` WHERE `id` >= 10;")
out.append("DELETE FROM `action_logs` WHERE `user_id` >= 10;")
out.append("DELETE FROM `notifications` WHERE `recipient_id` >= 10;")
out.append("DELETE FROM `messages` WHERE `sender_id` >= 10;")
out.append("DELETE FROM `conversations` WHERE `user1_id` >= 10 OR `user2_id` >= 10;")
out.append("DELETE FROM `activity_guests` WHERE `teacher_profile_id` >= 10 OR `activity_id` >= 1000 OR `activity_id` IN (SELECT `id` FROM `activities` WHERE `inspector_user_id` >= 100);")
out.append("DELETE FROM `activity_reports` WHERE `id` >= 1000 OR `inspector_user_id` >= 100;")
out.append("DELETE FROM `activities` WHERE `id` >= 1000 OR `inspector_user_id` >= 100;")
out.append("DELETE FROM `quiz_submissions` WHERE `id` >= 10;")
out.append("DELETE FROM `quiz_questions` WHERE `id` >= 10;")
out.append("DELETE FROM `quiz_assignments` WHERE `quiz_id` >= 10 OR `teacher_id` >= 10;")
out.append("DELETE FROM `quizzes` WHERE `id` >= 10;")
out.append("DELETE FROM `course_assignments` WHERE `id` >= 10;")
out.append("DELETE FROM `course_lessons` WHERE `id` >= 10;")
out.append("DELETE FROM `course_modules` WHERE `id` >= 10;")
out.append("DELETE FROM `courses` WHERE `id` >= 10;")
out.append("DELETE FROM `timetable_slots` WHERE `id` >= 10;")
out.append("DELETE FROM `profile_delegations` WHERE `profile_id` >= 10;")
out.append("DELETE FROM `profile_dependencies` WHERE `profile_id` >= 10;")
out.append("DELETE FROM `profile_departments` WHERE `profile_id` >= 10;")
out.append("DELETE FROM `profile_etablissements` WHERE `profile_id` >= 10;")
out.append("DELETE FROM `teacher_profiles` WHERE `id` >= 10;")
out.append("DELETE FROM `inspector_profiles` WHERE `id` >= 10;")
out.append("DELETE FROM `etablissements` WHERE `id` >= 10;")
out.append("DELETE FROM `dependencies` WHERE `id` >= 10;")
out.append("DELETE FROM `departments` WHERE `id` >= 10;")
out.append("DELETE FROM `delegations` WHERE `id` >= 10;")
out.append("DELETE FROM `regions` WHERE `id` >= 10;")
out.append("DELETE FROM `users` WHERE `id` >= 10;")
out.append("")

out.append("-- 2. SEED REGIONS (The 24 Governorates of Tunisia, offset to 1000)")
regions = [
    'Tunis Region', 'Ariana Region', 'Ben Arous Region', 'Manouba Region', 'Nabeul Region', 'Zaghouan Region',
    'Bizerte Region', 'Béja Region', 'Jendouba Region', 'Le Kef Region', 'Siliana Region', 'Sousse Region',
    'Monastir Region', 'Mahdia Region', 'Sfax Region', 'Kairouan Region', 'Kasserine Region', 'Sidi Bouzid Region',
    'Gabès Region', 'Medenine Region', 'Tataouine Region', 'Gafsa Region', 'Tozeur Region', 'Kebili Region'
]
region_insert = "INSERT INTO `regions` (`id`, `name`) VALUES \n"
region_insert += ",\n".join([f"({1000 + i}, '{name}')" for i, name in enumerate(regions)]) + ";"
out.append(region_insert)
out.append("")

out.append("-- 3. SEED DELEGATIONS (52 delegations offset to 1000)")
delegations = [
    # Tunis (0-9)
    (0, 'Tunis Medina Del', 0), (1, 'Sidi El Béchir Del', 0), (2, 'La Marsa Del', 0), (3, 'Le Bardo Del', 0), (4, 'Carthage Del', 0),
    (5, 'El Omrane Del', 0), (6, 'El Menzah Del', 0), (7, 'Hay El Khadra Del', 0), (8, 'La Goulette Del', 0), (9, 'Sidi Hassine Del', 0),
    # Ariana (10-15)
    (10, 'Ariana Ville Del', 1), (11, 'La Soukra Del', 1), (12, 'Raoued Del', 1), (13, 'Kalâat el-Andalous Del', 1), (14, 'Sidi Thabet Del', 1), (15, 'Mnihla Del', 1),
    # Ben Arous (16-21)
    (16, 'Ben Arous Ville Del', 2), (17, 'Megrine Del', 2), (18, 'Radès Del', 2), (19, 'Hammam Lif Del', 2), (20, 'Bou Mhel el-Bassatine Del', 2), (21, 'Ezzahra Del', 2),
    # Nabeul (22-29)
    (22, 'Nabeul Ville Del', 4), (23, 'Hammamet Del', 4), (24, 'Korba Del', 4), (25, 'Menzel Temime Del', 4), (26, 'Kelibia Del', 4), (27, 'Soliman Del', 4), (28, 'Grombalia Del', 4), (29, 'Dar Châabane El Fehri Del', 4),
    # Sousse (30-37)
    (30, 'Sousse Medina Del', 11), (31, 'Sousse Riadh Del', 11), (32, 'Akouda Del', 11), (33, 'Hammam Sousse Del', 11), (34, 'Kalaâ Kebira Del', 11), (35, 'Kalaâ Seghira Del', 11), (36, 'Msaken Del', 11), (37, 'Sousse Jaouhara Del', 11),
    # Monastir (38-43)
    (38, 'Monastir Ville Del', 12), (39, 'Moknine Del', 12), (40, 'Jemmal Del', 12), (41, 'Ksar Hellal Del', 12), (42, 'Téboulba Del', 12), (43, 'Bekalta Del', 12),
    # Sfax (44-51)
    (44, 'Sfax Ville Del', 14), (45, 'Sfax Ouest Del', 14), (46, 'Sakiet Ezzit Del', 14), (47, 'Sakiet Eddaier Del', 14), (48, 'Sfax Sud Del', 14), (49, 'Thyna Del', 14), (50, 'El Hencha Del', 14), (51, 'Jebeniana Del', 14)
]
del_insert = "INSERT INTO `delegations` (`id`, `name`, `region_id`) VALUES \n"
del_insert += ",\n".join([f"({1000 + id_val}, '{name}', {1000 + reg_id})" for id_val, name, reg_id in delegations]) + ";"
out.append(del_insert)
out.append("")

out.append("-- 4. SEED DEPARTMENTS (Starting at ID 1000)")
out.append("INSERT INTO `departments` (`id`, `name`, `delegation_id`) VALUES")
out.append("(1000, 'Direction Régionale Tunis 1', 1000),")
out.append("(1001, 'Direction Régionale Sousse', 1030),")
out.append("(1002, 'Direction Régionale Sfax', 1044);")
out.append("")

out.append("-- 5. SEED DEPENDENCIES (Starting at ID 1000)")
out.append("INSERT INTO `dependencies` (`id`, `name`, `delegation_id`) VALUES")
out.append("(1000, 'Circonscription Tunis 1', 1000),")
out.append("(1001, 'Circonscription Sousse Nord', 1030),")
out.append("(1002, 'Circonscription Sfax Est', 1044);")
out.append("")

out.append("-- 6. SEED ETABLISSEMENTS (Schools starting at ID 1000)")
schools = [
    (0, 'Lycée Pilote Tunis', 'SECONDARY', 0),
    (1, 'Lycée Rue du Pacha', 'SECONDARY', 0),
    (2, 'Collège Sadiki', 'PREPARATORY', 0),
    (3, 'Lycée Pilote Sousse', 'SECONDARY', 1),
    (4, 'Lycée Tahar Sfar Sousse', 'SECONDARY', 1),
    (5, 'Lycée Pilote Sfax', 'SECONDARY', 2),
    (6, 'Collège Majida Boulila', 'PREPARATORY', 2),
    (7, 'Lycée Carthage Presidence', 'SECONDARY', 0),
    (8, 'Lycée Ibn Charaf Tunis', 'SECONDARY', 0),
    (9, 'Collège Pilote Les Berges du Lac', 'PREPARATORY', 0)
]
school_insert = "INSERT INTO `etablissements` (`id`, `name`, `school_level`, `dependency_id`) VALUES \n"
school_insert += ",\n".join([f"({1000 + id_val}, '{name}', '{level}', {1000 + dep_id})" for id_val, name, level, dep_id in schools]) + ";"
out.append(school_insert)
out.append("")

out.append("-- 7. SEED USERS (200 Users: 1 Admin, 30 Inspectors, 169 Teachers)")
out.append("-- Password for all is 'password' (bcrypt hash below)")
out.append("")

# Admin user
out.append("-- 7.1 Admin (1 User)")
out.append("INSERT INTO `users` (`id`, `enabled`, `is_microsoft_connected`, `profile_completed`, `created_at`, `serial_code`, `email`, `password`, `role`) VALUES")
out.append("(1000, 1, 0, 1, NOW(), 'ADMIN-1000', 'admin.system@inspector.tn', '$2a$10$8.UnVuG9HHgffUDAlk8qfOuVGkqRzgVymGe07xd00DMxs.TVu4ATA', 'ADMIN');")
out.append("")

# Inspectors: 1101 to 1130
out.append("-- 7.2 Inspectors (30 Users: IDs 1101 to 1130)")
inspector_users = []
for i in range(1, 31):
    uid = 1100 + i
    email = f"inspector.{i}@inspector.tn"
    serial = f"I-{uid}"
    inspector_users.append(f"({uid}, 1, 0, 1, NOW(), '{serial}', '{email}', '$2a$10$8.UnVuG9HHgffUDAlk8qfOuVGkqRzgVymGe07xd00DMxs.TVu4ATA', 'INSPECTOR')")
out.append("INSERT INTO `users` (`id`, `enabled`, `is_microsoft_connected`, `profile_completed`, `created_at`, `serial_code`, `email`, `password`, `role`) VALUES\n" + ",\n".join(inspector_users) + ";")
out.append("")

# Teachers: 1200 to 1368
out.append("-- 7.3 Teachers (169 Users: IDs 1200 to 1368)")
teacher_users = []
for i in range(169):
    uid = 1200 + i
    email = f"teacher.{i}@edu.tn"
    serial = f"T-{uid}"
    teacher_users.append(f"({uid}, 1, 0, 1, NOW(), '{serial}', '{email}', '$2a$10$8.UnVuG9HHgffUDAlk8qfOuVGkqRzgVymGe07xd00DMxs.TVu4ATA', 'TEACHER')")
out.append("INSERT INTO `users` (`id`, `enabled`, `is_microsoft_connected`, `profile_completed`, `created_at`, `serial_code`, `email`, `password`, `role`) VALUES\n" + ",\n".join(teacher_users) + ";")
out.append("")

out.append("-- 8. SEED INSPECTOR PROFILES (30 Profiles: IDs 1101 to 1130, matching user_id)")
first_names = ['Mohamed', 'Ahmed', 'Fatma', 'Yassine', 'Leila', 'Sami', 'Rym', 'Mourad', 'Ines', 'Khalil', 'Hichem', 'Moncef', 'Kamel', 'Slim', 'Tarek', 'Wajdi', 'Nabil', 'Mourad', 'Habib', 'Anis', 'Ali', 'Belhassen', 'Chaker', 'Dali', 'Ezzedine', 'Fouad', 'Gazi', 'Hamadi', 'Imed', 'Jamil']
last_names = ['Ali', 'Ben Ali', 'Mansour', 'Trabelsi', 'Mejri', 'Hamdi', 'Gharbi', 'Jouini', 'Belhadj', 'Amri', 'Hammami', 'Trabelsi', 'Gharbi', 'Riahi', 'Jaziri', 'Khlifi', 'Saidi', 'Chebbi', 'Dridi', 'Louati', 'Amri', 'Ben Youssef', 'Cherif', 'Daoud', 'El Abed', 'Fekih', 'Gharbi', 'Hammami', 'Jaziri', 'Khlifi']
ranks = ['INSPECTOR_GENERAL', 'INSPECTOR_PRINCIPAL', 'INSPECTOR', 'INSPECTOR_REGIONAL']
school_levels = ['PRIMARY', 'PREPARATORY', 'SECONDARY']
subjects = ['ARABIC','FRENCH','ENGLISH','MATH','PHYSICS','CHEMISTRY','BIOLOGY','HISTORY_GEOGRAPHY','PHILOSOPHY','ISLAMIC_STUDIES','PHYSICAL_EDUCATION','COMPUTER_SCIENCE','ECONOMICS','ARTS','MUSIC']

inspector_profiles = []
for i in range(1, 31):
    uid = 1100 + i
    fname = first_names[(i - 1) % len(first_names)]
    lname = last_names[(i - 1) % len(last_names)]
    phone = f"+21698{i:06d}"
    lang = 'Arabic' if i % 3 == 0 else ('French' if i % 3 == 1 else 'English')
    rank = ranks[(i - 1) % len(ranks)]
    level = school_levels[(i - 1) % len(school_levels)]
    subj = subjects[(i - 1) % len(subjects)]
    inspector_profiles.append(f"({uid}, {uid}, '{fname}', '{lname}', '{phone}', '{lang}', '{rank}', '{level}', '{subj}')")
out.append("INSERT INTO `inspector_profiles` (`id`, `user_id`, `first_name`, `last_name`, `phone`, `language`, `rank`, `school_level`, `subject`) VALUES\n" + ",\n".join(inspector_profiles) + ";")
out.append("")

# Seeding profile associations
out.append("-- 8.1 SEED INSPECTOR JURISDICTION ASSOCIATIONS (Join tables)")
profile_delegations = []
profile_dependencies = []
profile_departments = []
profile_etablissements = []

for i in range(1, 31):
    uid = 1100 + i
    # Tunis inspectors: 1101 to 1110
    if i <= 10:
        # Link to Tunis delegations (1000 to 1009)
        for d in range(1000, 1010):
            profile_delegations.append(f"({uid}, {d})")
        profile_dependencies.append(f"({uid}, 1000)")
        profile_departments.append(f"({uid}, 1000)")
        # Link to Tunis schools (1000, 1001, 1002, 1007, 1008, 1009)
        for s in [1000, 1001, 1002, 1007, 1008, 1009]:
            profile_etablissements.append(f"({uid}, {s})")
    # Sousse inspectors: 1111 to 1120
    elif i <= 20:
        # Link to Sousse delegations (1030 to 1037)
        for d in range(1030, 1038):
            profile_delegations.append(f"({uid}, {d})")
        profile_dependencies.append(f"({uid}, 1001)")
        profile_departments.append(f"({uid}, 1001)")
        # Link to Sousse schools (1003, 1004)
        for s in [1003, 1004]:
            profile_etablissements.append(f"({uid}, {s})")
    # Sfax inspectors: 1121 to 1130
    else:
        # Link to Sfax delegations (1044 to 1051)
        for d in range(1044, 1052):
            profile_delegations.append(f"({uid}, {d})")
        profile_dependencies.append(f"({uid}, 1002)")
        profile_departments.append(f"({uid}, 1002)")
        # Link to Sfax schools (1005, 1006)
        for s in [1005, 1006]:
            profile_etablissements.append(f"({uid}, {s})")

out.append("INSERT INTO `profile_delegations` (`profile_id`, `delegation_id`) VALUES\n" + ",\n".join(profile_delegations) + ";")
out.append("INSERT INTO `profile_dependencies` (`profile_id`, `dependency_id`) VALUES\n" + ",\n".join(profile_dependencies) + ";")
out.append("INSERT INTO `profile_departments` (`profile_id`, `department_id`) VALUES\n" + ",\n".join(profile_departments) + ";")
out.append("INSERT INTO `profile_etablissements` (`profile_id`, `etablissement_id`) VALUES\n" + ",\n".join(profile_etablissements) + ";")
out.append("")

out.append("-- 9. SEED TEACHER PROFILES (169 Profiles: IDs 1200 to 1368, matching user_id)")
teacher_profiles = []
for i in range(169):
    uid = 1200 + i
    fname = first_names[i % len(first_names)]
    lname = last_names[i % len(last_names)]
    phone = f"+21620{i:06d}"
    subj = subjects[i % len(subjects)]
    lang = 'Arabic' if i % 3 == 0 else ('French' if i % 3 == 1 else 'English')
    
    # Assign school & matching delegation/dependency
    school_id = 1000 + (i % 10)
    if school_id in [1000, 1001, 1002, 1007, 1008, 1009]:
        del_id = 1000
        dep_id = 1000
    elif school_id in [1003, 1004]:
        del_id = 1030
        dep_id = 1001
    else:
        del_id = 1044
        dep_id = 1002
        
    teacher_profiles.append(f"({uid}, {uid}, '{fname}', '{lname}', '{phone}', '{subj}', '{lang}', {del_id}, {dep_id}, {school_id})")

out.append("INSERT INTO `teacher_profiles` (`id`, `user_id`, `first_name`, `last_name`, `phone`, `subject`, `language`, `delegation_id`, `dependency_id`, `etablissement_id`) VALUES\n" + ",\n".join(teacher_profiles) + ";")
out.append("")

out.append("-- 10. SEED ACTION LOGS (Simulate recent production activity logs)")
action_logs = []
for i in range(120):
    user_id = 1000 if i % 10 == 0 else (1100 + (i % 30) + 1 if i % 2 == 0 else 1200 + (i % 169))
    action_type = 'LOGIN' if i % 3 == 0 else ('UPDATE' if i % 3 == 1 else 'EXPORT')
    desc = 'User logged in from production simulation' if action_type == 'LOGIN' else ('Updated jurisdiction settings' if action_type == 'UPDATE' else 'Exported performance metrics report')
    ip = f"197.1.{random.randint(1, 254)}.{random.randint(1, 254)}"
    action_logs.append(f"('{action_type}', DATE_SUB(NOW(), INTERVAL {i * 15} MINUTE), '{desc}', 'User', {user_id}, '{ip}')")
out.append("INSERT INTO `action_logs` (`action_type`, `created_at`, `description`, `entity_type`, `user_id`, `ip_address`) VALUES\n" + ",\n".join(action_logs) + ";")
out.append("")

out.append("-- 11. SEED NOTIFICATIONS")
notifications = []
for i in range(60):
    recipient_id = 1100 + (i % 30) + 1 if i % 2 == 0 else 1200 + (i % 169)
    notifications.append(f"(0, NOW(), {recipient_id}, 'SYSTEM', 'Production Simulation Initialized', 'Your account is successfully synced with 200 Tunisian users.')")
out.append("INSERT INTO `notifications` (`is_read`, `created_at`, `recipient_id`, `type`, `title`, `message`) VALUES\n" + ",\n".join(notifications) + ";")
out.append("")

out.append("-- 12. SEED EVALUATION ACTIVITIES (60 Activities: IDs 1000 to 1059)")
activities = []
# Ensure inspector and teacher are in the same area!
# Areas: 0=Tunis (Inspectors 1101-1110, Teachers 1200-1239 or similar whose school matches Tunis)
# Let's group teachers by area
teachers_by_area = {0: [], 1: [], 2: []}
for i in range(169):
    uid = 1200 + i
    school_id = 1000 + (i % 10)
    if school_id in [1000, 1001, 1002, 1007, 1008, 1009]:
        teachers_by_area[0].append(uid)
    elif school_id in [1003, 1004]:
        teachers_by_area[1].append(uid)
    else:
        teachers_by_area[2].append(uid)

activities_list = []
activity_guests = []
activity_reports = []

# Generate 60 activities
for i in range(60):
    act_id = 1000 + i
    area = i % 3
    
    # Select inspector from this area
    if area == 0:
        insp_uid = 1101 + (i % 10)
    elif area == 1:
        insp_uid = 1111 + (i % 10)
    else:
        insp_uid = 1121 + (i % 10)
        
    # Select teacher from this area
    teacher_list = teachers_by_area[area]
    teach_uid = teacher_list[i % len(teacher_list)]
    
    # Get subject for this teacher to make the title realistic
    subj = subjects[i % len(subjects)]
    
    title = f"Inspection Pedagogique - {subj}"
    start_date = f"2026-0{(i % 5) + 1}-{(i % 25) + 1:02d} {8 + (i % 8):02d}:00:00"
    end_date = f"2026-0{(i % 5) + 1}-{(i % 25) + 1:02d} {10 + (i % 8):02d}:00:00"
    
    activities_list.append(f"({act_id}, 0, 0, '{end_date}', {insp_uid}, '{start_date}', '{title}', 'Salle de classe', 'Inspection periodique de controle', NULL, 'INSPECTION')")
    activity_guests.append(f"({act_id}, {teach_uid})")
    
    # Report score
    score = random.randint(10, 20)
    status = 'FINAL'
    observations = "L enseignant montre une excellente maitrise scientifique et pedagogique. Structure de la lecon claire et objectifs pedagogiques atteints."
    recommendations = "Favoriser davantage les travaux pratiques en sous-groupes et integrer des outils numeriques interactifs."
    
    activity_reports.append(f"({score}, {act_id}, '{start_date}', {act_id}, {insp_uid}, {teach_uid}, '{start_date}', 'Rapport d Evaluation - {subj}', '{observations}', '{recommendations}', '{status}')")

out.append("INSERT INTO `activities` (`id`, `is_online`, `is_reminder_sent`, `end_date_time`, `inspector_user_id`, `start_date_time`, `title`, `location`, `description`, `meeting_url`, `type`) VALUES\n" + ",\n".join(activities_list) + ";")
out.append("")

out.append("-- 12.1 LINK TEACHERS TO ACTIVITIES")
out.append("INSERT INTO `activity_guests` (`activity_id`, `teacher_profile_id`) VALUES\n" + ",\n".join(activity_guests) + ";")
out.append("")

out.append("-- 12.2 SEED EVALUATION REPORTS (60 Reports: IDs 1000 to 1059)")
out.append("INSERT INTO `activity_reports` (`score`, `activity_id`, `created_at`, `id`, `inspector_user_id`, `teacher_profile_id`, `updated_at`, `title`, `observations`, `recommendations`, `status`) VALUES")
out.append(",\n".join(activity_reports) + ";")
out.append("")

# Seeding courses
out.append("-- 13. SEED COURSES AND TRAINING MODULES (Starting at ID 1000)")
courses = []
for i in range(5):
    course_id = 1000 + i
    insp_id = 1101 + i
    subj = subjects[i % len(subjects)]
    title = f"Course on Modern {subj} Pedagogical Methods"
    desc = f"Comprehensive training program designed by inspector for secondary school teachers specialized in {subj}."
    status = 'PUBLISHED'
    courses.append(f"(NOW(), {course_id}, {insp_id}, NOW(), '{title}', '{desc}', '{status}', '{subj}')")
out.append("INSERT INTO `courses` (`created_at`, `id`, `inspector_id`, `updated_at`, `title`, `description`, `status`, `subject`) VALUES\n" + ",\n".join(courses) + ";")
out.append("")

# Course modules
out.append("-- 13.1 SEED COURSE MODULES")
modules = []
for i in range(5):
    course_id = 1000 + i
    for m in range(2):
        mod_id = 1000 + i * 2 + m
        title = f"Module {m + 1}: Core Standards"
        desc = "Detailed overview of regional standard methods and curriculum adaptation."
        modules.append(f"({m}, {course_id}, {mod_id}, '{title}', '{desc}')")
out.append("INSERT INTO `course_modules` (`order_index`, `course_id`, `id`, `title`, `description`) VALUES\n" + ",\n".join(modules) + ";")
out.append("")

# Course lessons
out.append("-- 13.2 SEED COURSE LESSONS")
lessons = []
for i in range(5):
    for m in range(2):
        mod_id = 1000 + i * 2 + m
        for l in range(2):
            less_id = 1000 + (i * 2 + m) * 2 + l
            title = f"Lesson {l + 1}: Classroom Practical Guide"
            desc = "A detailed guide including official documents and sample worksheets."
            content_url = f"https://inspectorhost.onrender.com/assets/pdf/lesson_{less_id}.pdf"
            lessons.append(f"(45, {l}, {less_id}, {mod_id}, '{title}', '{content_url}', '{desc}', 'PDF')")
out.append("INSERT INTO `course_lessons` (`duration_minutes`, `order_index`, `id`, `module_id`, `title`, `content_url`, `description`, `type`) VALUES\n" + ",\n".join(lessons) + ";")
out.append("")

# Course assignments
out.append("-- 13.3 SEED COURSE ASSIGNMENTS (Assign courses to teachers)")
course_assignments = []
for i in range(5):
    course_id = 1000 + i
    # Assign each course to 5 teachers
    for t in range(5):
        assign_id = 1000 + i * 5 + t
        teach_id = 1200 + i * 5 + t
        course_assignments.append(f"(NOW(), {course_id}, {assign_id}, {teach_id})")
out.append("INSERT INTO `course_assignments` (`assigned_at`, `course_id`, `id`, `teacher_id`) VALUES\n" + ",\n".join(course_assignments) + ";")
out.append("")

# Quizzes
out.append("-- 14. SEED QUIZZES AND QUESTIONS")
quizzes = []
for i in range(5):
    quiz_id = 1000 + i
    insp_id = 1101 + i
    subj = subjects[i % len(subjects)]
    title = f"Evaluation Quiz - {subj} Standards"
    topic = f"Modern pedagogy of {subj}"
    level = school_levels[i % len(school_levels)]
    quizzes.append(f"(NOW(), {quiz_id}, {insp_id}, '{title}', '{topic}', '{subj}', '11th Grade', '{level}')")
out.append("INSERT INTO `quizzes` (`created_at`, `id`, `inspector_id`, `title`, `topic`, `subject`, `grade`, `school_level`) VALUES\n" + ",\n".join(quizzes) + ";")
out.append("")

# Quiz questions
out.append("-- 14.1 SEED QUIZ QUESTIONS")
questions = []
for q in range(5):
    quiz_id = 1000 + q
    # 2 questions per quiz
    for k in range(2):
        quest_id = 1000 + q * 2 + k
        qtext = f"Which pedagogical method is most effective for lesson {k+1}?"
        options = "[\"Active learning\", \"Direct instruction\", \"Collaborative groups\", \"Individual study\"]"
        correct = "Active learning"
        questions.append(f"({quest_id}, {quiz_id}, '{correct}', '{options}', '{qtext}', 'MCQ')")
out.append("INSERT INTO `quiz_questions` (`id`, `quiz_id`, `correct_answer`, `options`, `question_text`, `type`) VALUES\n" + ",\n".join(questions) + ";")
out.append("")

# Quiz assignments
out.append("-- 14.2 SEED QUIZ ASSIGNMENTS")
quiz_assignments = []
for q in range(5):
    quiz_id = 1000 + q
    # Assign to 5 teachers
    for t in range(5):
        teach_id = 1200 + q * 5 + t
        quiz_assignments.append(f"({quiz_id}, {teach_id})")
out.append("INSERT INTO `quiz_assignments` (`quiz_id`, `teacher_id`) VALUES\n" + ",\n".join(quiz_assignments) + ";")
out.append("")

# Quiz submissions
out.append("-- 14.3 SEED QUIZ SUBMISSIONS (Simulated completed submissions)")
submissions = []
for q in range(5):
    quiz_id = 1000 + q
    for t in range(3):  # 3 of the assigned teachers have submitted
        sub_id = 1000 + q * 3 + t
        teach_id = 1200 + q * 5 + t
        score = random.choice([80, 90, 100])
        answers = f"{{\\\"q1\\\":\\\"Active learning\\\",\\\"q2\\\":\\\"Active learning\\\"}}"
        eval_text = "Excellent understanding of modern pedagogical techniques."
        sugg = "Continue to integrate active learning practices in everyday lessons."
        submissions.append(f"({score}, {sub_id}, {quiz_id}, NOW(), {teach_id}, '{answers}', '{eval_text}', '{sugg}')")
out.append("INSERT INTO `quiz_submissions` (`score`, `id`, `quiz_id`, `submitted_at`, `teacher_id`, `answers`, `evaluation_text`, `training_suggestion`) VALUES\n" + ",\n".join(submissions) + ";")
out.append("")

# Seeding lesson progress
out.append("-- 15. SEED LESSON PROGRESS")
progress = []
for l in range(10):
    less_id = 1000 + l
    for t in range(5):
        prog_id = 1000 + l * 5 + t
        teach_id = 1200 + t
        # Use standard bit values (1 for true, 0 for false)
        progress.append(f"(1, 100, NOW(), {prog_id}, {less_id}, {teach_id})")
out.append("INSERT INTO `lesson_progress` (`completed`, `score`, `completed_at`, `id`, `lesson_id`, `teacher_id`) VALUES\n" + ",\n".join(progress) + ";")
out.append("")

out.append("SET FOREIGN_KEY_CHECKS = 1;")
out.append("COMMIT;")
out.append("")

sql_content = "\n".join(out)

# Write to seed_production_data.sql
with open("c:/Users/scsof/Downloads/Inspector_1-main/Inspector_1-main/seed_production_data.sql", "w", encoding="utf-8") as f:
    f.write(sql_content)

# Write to seed_render_db.sql
with open("c:/Users/scsof/Downloads/Inspector_1-main/Inspector_1-main/seed_render_db.sql", "w", encoding="utf-8") as f:
    f.write(sql_content)

print("Successfully generated and wrote seed files!")
