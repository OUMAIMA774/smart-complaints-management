-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : jeu. 18 juin 2026 à 02:10
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `gestion_reclamations`
--

-- --------------------------------------------------------

--
-- Structure de la table `citoyens`
--

CREATE TABLE `citoyens` (
  `id` int(11) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) NOT NULL,
  `cin` varchar(20) NOT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `date_creation` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `citoyens`
--

INSERT INTO `citoyens` (`id`, `nom`, `prenom`, `cin`, `telephone`, `email`, `date_creation`) VALUES
(1, 'EL YAMANI', 'OUMAIMA', 'AB123456', '0680945027', 'elyamanioumaimaa@gmail.com', '2026-05-04 13:13:01'),
(2, 'Amrani', 'Youssef', 'GH445566', '0645678901', 'youssef@gmail.com', '2026-05-04 13:16:41'),
(3, 'Idrissi', 'Idrissi', 'IJ778899', '0656789012', 'salma@gmail.com', '2026-05-05 11:52:33'),
(4, 'EL YAMAN', 'OUMAIM', 'IJ778897', '0680945027', 'elyamanioumamaa@gmail.com', '2026-05-05 12:12:05'),
(5, 'EL YAMA', 'Oumayma', 'IJ777777', '0680945028', 'elyamanimaimaa@gmail.com', '2026-05-05 12:31:52'),
(6, 'EL YAMANI', 'DOAE', 'G767902', '0680945027', 'elyamanidoae@gmail.com', '2026-05-12 11:45:39'),
(7, 'EL YAMANI', 'mohamed', 'G767901', '+212680945027', 'elyamanimohamed@gmail.com', '2026-05-12 13:02:24'),
(8, 'EL YAMANI', 'mohamed', 'G767901', '+212680945027', 'elyamanimohamed@gmail.com', '2026-05-12 13:04:50'),
(9, 'EL YAMANI', 'mohamed', 'G767903', '+212680945028', 'elyamanimohamed@gmail.com', '2026-05-18 13:10:36'),
(10, 'BENALI', 'SARA', 'CD458921', '0678123456', 'sara.benali@gmail.com', '2026-05-18 13:20:12'),
(12, 'EL YAMANI', 'Chouaib', 'G767904', '+212680945080', 'elyamanichouaib@gmail.com', '2026-06-01 01:32:11'),
(13, 'EL YAMANI', 'Chouaib', 'G767904', '+212680945080', 'elyamanichouaib@gmail.com', '2026-06-01 01:33:35'),
(14, 'EL YAMANI', 'Chouaib', 'G767904', '+212680945080', 'elyamanichouaib@gmail.com', '2026-06-01 01:35:06'),
(15, 'EL YAMANI', 'omniya', 'G767905', '+212680945005', 'elyamaniomniya@gmail.com', '2026-06-01 02:00:15'),
(16, 'EL YAMANI', 'amina', 'G767907', '+212680945077', 'elyamanamina@gmail.com', '2026-06-01 03:57:00'),
(17, 'EL YAMANI', 'amin', 'G12345', '+212680945027', 'elyamaniamin@gmail.com', '2026-06-02 11:13:42'),
(18, 'EL YAMANI', 'OUMAIMA', 'G767902', '+212680945027', 'elyamanioumaimaa@gmail.com', '2026-06-02 11:33:44'),
(19, 'EL YAMANI', 'OUMAIMA', 'G767902', '+212680945027', 'elyamanioumaimaa@gmail.com', '2026-06-02 11:37:59'),
(20, 'EL YAMANI', 'DOAA', 'AB123456', '+212680945077', 'elyamanidoaa@gmail.com', '2026-06-15 22:00:17'),
(21, 'EL YAMANI', 'OUMAIMA', 'G767902', '+212680945027', 'elyamanioumaimaa@gmail.com', '2026-06-16 00:49:10'),
(22, 'EL YAMANI', 'OUMAIMA', 'G767902', '+212680945027', 'elyamanioumaimaa@gmail.com', '2026-06-16 00:51:29'),
(23, 'EL YAMANI', 'mohamaed', 'G767900', '+212680945027', 'elyamanimohamed@gmail.com', '2026-06-16 01:43:33');

-- --------------------------------------------------------

--
-- Structure de la table `divisions`
--

CREATE TABLE `divisions` (
  `id` int(11) NOT NULL,
  `nom_division` varchar(100) NOT NULL,
  `categorie_associee` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `divisions`
--

INSERT INTO `divisions` (`id`, `nom_division`, `categorie_associee`) VALUES
(1, 'Division Éclairage Public', 'eclairage'),
(2, 'Division Eau', 'eau'),
(3, 'Division Voirie', 'voirie'),
(4, 'Division Propreté', 'proprete'),
(5, 'Division Assainissement', 'assainissement');

-- --------------------------------------------------------

--
-- Structure de la table `historique_reclamations`
--

CREATE TABLE `historique_reclamations` (
  `id` int(11) NOT NULL,
  `reclamation_id` int(11) NOT NULL,
  `action` varchar(255) NOT NULL,
  `ancien_statut` varchar(100) DEFAULT NULL,
  `nouveau_statut` varchar(100) DEFAULT NULL,
  `ancienne_division` int(11) DEFAULT NULL,
  `nouvelle_division` int(11) DEFAULT NULL,
  `utilisateur_id` int(11) DEFAULT NULL,
  `date_action` datetime DEFAULT current_timestamp(),
  `commentaire` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `historique_reclamations`
--

INSERT INTO `historique_reclamations` (`id`, `reclamation_id`, `action`, `ancien_statut`, `nouveau_statut`, `ancienne_division`, `nouvelle_division`, `utilisateur_id`, `date_action`, `commentaire`) VALUES
(4, 4, 'Réclamation déposée, classifiée automatiquement en \'eau\' avec priorité \'urgente\'', NULL, 'nouvelle', NULL, 2, NULL, '2026-05-05 12:12:05', NULL),
(5, 5, 'Réclamation déposée, classifiée automatiquement en \'eclairage\' avec priorité \'faible\'', NULL, 'nouvelle', NULL, 1, NULL, '2026-05-05 12:31:52', NULL),
(6, 5, 'Réponse envoyée au citoyen', 'en_cours', 'repondue', NULL, NULL, NULL, '2026-05-05 12:52:00', NULL),
(7, 6, 'Réclamation déposée, classifiée automatiquement en \'eclairage\' avec priorité \'faible\'', NULL, 'nouvelle', NULL, 1, NULL, '2026-05-12 11:45:39', NULL),
(8, 7, 'Réclamation déposée, classifiée automatiquement en \'voirie\' avec priorité \'urgente\'', NULL, 'nouvelle', NULL, 3, NULL, '2026-05-12 13:02:24', NULL),
(9, 8, 'Réclamation déposée, classifiée automatiquement en \'voirie\' avec priorité \'urgente\'', NULL, 'nouvelle', NULL, 3, NULL, '2026-05-12 13:04:50', NULL),
(10, 5, 'Réclamation clôturée par la commune après traitement', 'repondue', 'cloturee', NULL, NULL, NULL, '2026-05-18 12:27:01', NULL),
(11, 6, 'Réponse envoyée au citoyen par la division', 'nouvelle', 'repondue', NULL, NULL, NULL, '2026-05-18 12:32:14', NULL),
(12, 9, 'Réclamation déposée, classifiée automatiquement en \'eclairage\' avec priorité \'urgente\'', NULL, 'nouvelle', NULL, 1, NULL, '2026-05-18 13:10:36', NULL),
(13, 9, 'Réclamation transférée de Division Éclairage Public vers Division Eau', 'nouvelle', 'en_cours', 1, 2, NULL, '2026-05-18 13:12:08', 'La réclamation concerne principalement une fuite d’eau nécessitant l’intervention de la Division Eau.'),
(14, 10, 'Réclamation déposée, classifiée automatiquement en \'voirie\' avec priorité \'urgente\'', NULL, 'nouvelle', NULL, 3, NULL, '2026-05-18 13:20:12', NULL),
(15, 10, 'Réclamation transférée de Division Voirie vers Division Assainissement', 'nouvelle', 'nouvelle', 3, 5, NULL, '2026-05-18 13:21:10', 'La dégradation de la chaussée est causée par un problème principal d’assainissement et de débordement d’égouts.'),
(16, 12, 'Réclamation déposée, classifiée automatiquement en \'eclairage\' avec priorité \'moyenne\'', NULL, 'nouvelle', NULL, 1, NULL, '2026-06-01 01:32:11', NULL),
(17, 13, 'Réclamation déposée, classifiée automatiquement en \'eclairage\' avec priorité \'moyenne\'', NULL, 'nouvelle', NULL, 1, NULL, '2026-06-01 01:33:35', NULL),
(18, 14, 'Réclamation déposée, classifiée automatiquement en \'eclairage\' avec priorité \'moyenne\'', NULL, 'nouvelle', NULL, 1, NULL, '2026-06-01 01:35:06', NULL),
(19, 15, 'Réclamation déposée, classifiée automatiquement en \'eclairage\' avec priorité \'urgente\'', NULL, 'nouvelle', NULL, 1, NULL, '2026-06-01 02:00:15', NULL),
(20, 16, 'Réclamation déposée, classifiée automatiquement en \'voirie\' avec priorité \'urgente\'', NULL, 'nouvelle', NULL, 3, NULL, '2026-06-01 03:57:00', NULL),
(21, 17, 'Réclamation déposée, classifiée automatiquement en \'eclairage\' avec priorité \'moyenne\'', NULL, 'nouvelle', NULL, 1, NULL, '2026-06-02 11:13:42', NULL),
(22, 6, 'Réclamation clôturée par la commune après traitement', 'repondue', 'cloturee', NULL, NULL, NULL, '2026-06-02 11:18:00', NULL),
(23, 18, 'Réclamation déposée, classifiée automatiquement en \'eclairage\' avec priorité \'faible\'', NULL, 'nouvelle', NULL, 1, NULL, '2026-06-02 11:33:44', NULL),
(24, 19, 'Réclamation déposée, classifiée automatiquement en \'eau\' avec priorité \'faible\'', NULL, 'nouvelle', NULL, 2, NULL, '2026-06-02 11:37:59', NULL),
(25, 20, 'Réclamation déposée, classifiée automatiquement en \'eclairage\' avec priorité \'urgente\'', NULL, 'nouvelle', NULL, 1, NULL, '2026-06-15 22:00:17', NULL),
(26, 20, 'Réponse envoyée au citoyen par la division', 'nouvelle', 'repondue', NULL, NULL, NULL, '2026-06-16 00:47:09', NULL),
(27, 20, 'Réclamation clôturée par la commune après traitement', 'repondue', 'cloturee', NULL, NULL, NULL, '2026-06-16 00:47:43', NULL),
(28, 21, 'Réclamation déposée, classifiée automatiquement en \'voirie\' avec priorité \'urgente\'', NULL, 'nouvelle', NULL, 3, NULL, '2026-06-16 00:49:10', NULL),
(29, 22, 'Réclamation déposée, classifiée automatiquement en \'eclairage\' avec priorité \'urgente\'', NULL, 'nouvelle', NULL, 1, NULL, '2026-06-16 00:51:29', NULL),
(30, 22, 'Réclamation transférée de Division Éclairage Public vers Division Eau', 'nouvelle', 'nouvelle', 1, 2, NULL, '2026-06-16 00:53:27', 'Après analyse de la réclamation, il apparaît que les dysfonctionnements signalés de l\'éclairage public sont probablement causés par une fuite d\'eau située à proximité des installations concernées. Le traitement de la cause principale relève de la compétence de la Division Eau. La réclamation est donc transférée à cette division pour prise en charge et intervention appropriée.\r\n'),
(31, 23, 'Réclamation déposée, classifiée automatiquement en \'eclairage\' avec priorité \'urgente\'', NULL, 'nouvelle', NULL, 1, NULL, '2026-06-16 01:43:33', NULL);

-- --------------------------------------------------------

--
-- Structure de la table `reclamations`
--

CREATE TABLE `reclamations` (
  `id` int(11) NOT NULL,
  `code_reclamation` varchar(50) NOT NULL,
  `citoyen_id` int(11) NOT NULL,
  `zone` varchar(100) DEFAULT NULL,
  `objet` varchar(150) DEFAULT NULL,
  `description` text NOT NULL,
  `categorie_predite` varchar(100) DEFAULT NULL,
  `priorite` enum('faible','moyenne','elevee','urgente') DEFAULT 'moyenne',
  `score_priorite` int(11) DEFAULT 0,
  `division_id` int(11) DEFAULT NULL,
  `statut` enum('nouvelle','en_cours','transferee','repondue','cloturee') DEFAULT 'nouvelle',
  `fichier_joint` varchar(255) DEFAULT NULL,
  `date_creation` datetime DEFAULT current_timestamp(),
  `est_transferee` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `reclamations`
--

INSERT INTO `reclamations` (`id`, `code_reclamation`, `citoyen_id`, `zone`, `objet`, `description`, `categorie_predite`, `priorite`, `score_priorite`, `division_id`, `statut`, `fichier_joint`, `date_creation`, `est_transferee`) VALUES
(4, 'REC-2026-0004', 4, 'centre', 'fuite', 'Il y a une fuite d’eau dangereuse devant une école', 'eau', 'urgente', 90, 2, 'nouvelle', NULL, '2026-05-05 12:12:05', 0),
(5, 'REC-2026-0005', 5, 'birami', 'prob', 'Le quartier reste dans le noir depuis plusieurs nuits', 'eclairage', 'faible', 30, 1, 'cloturee', 'REC-2026-0005_1.png', '2026-05-05 12:31:52', 0),
(6, 'REC-2026-0006', 6, 'centre ville', 'La rue est très sombre après le coucher du soleil.', 'Le quartier reste dans le noir depuis plusieurs nuits et les habitants ne se sentent plus en sécurité.', 'eclairage', 'faible', 30, 1, 'cloturee', 'REC-2026-0006_rue.jfif', '2026-05-12 11:45:39', 0),
(7, 'REC-2026-0007', 7, 'Hay Nakhil', 'Fuite d’eau importante devant les habitations', 'Une fuite d’eau importante est présente depuis plusieurs jours devant plusieurs maisons du quartier. L’eau s’accumule sur la route et empêche les habitants de circuler normalement. La situation devient dangereuse pour les véhicules et les piétons.', 'voirie', 'urgente', 90, 3, 'nouvelle', 'REC-2026-0007_fuite.jfif', '2026-05-12 13:02:24', 0),
(8, 'REC-2026-0008', 8, 'Hay Nakhil', 'Fuite d’eau importante devant les habitations', 'Une fuite d’eau importante est présente depuis plusieurs jours devant plusieurs maisons du quartier. L’eau s’accumule sur la route et empêche les habitants de circuler normalement. La situation devient dangereuse pour les véhicules et les piétons.', 'voirie', 'urgente', 90, 3, 'nouvelle', 'REC-2026-0008_fuite.jfif', '2026-05-12 13:04:50', 0),
(9, 'REC-2026-0009', 9, 'Centre Ville', 'Poteau endommagé avec fuite d’eau et éclairage défaillant', 'Depuis plusieurs jours, un poteau d’éclairage public situé près de la fontaine au centre-ville est endommagé. \r\nL’éclairage ne fonctionne plus correctement la nuit et une fuite d’eau importante est également visible à sa base, provoquant une accumulation d’eau sur la chaussée. \r\nCette situation représente un danger pour les passants et complique la circulation dans la zone.', 'eclairage', 'urgente', 90, 2, 'en_cours', 'REC-2026-0009_poteau.jfif', '2026-05-18 13:10:36', 0),
(10, 'REC-2026-0010', 10, 'Hay Akkari', 'Chaussée endommagée et égout débordant devant l’école', 'Depuis environ une semaine, la route devant l’école primaire de Hay Akkari est fortement dégradée à cause d’un débordement continu des égouts. \r\nL’eau usée s’accumule sur la chaussée, provoque des odeurs désagréables et rend la circulation difficile pour les élèves et les habitants. \r\nPlusieurs lampadaires à proximité sont aussi éclaboussés, mais le problème principal semble venir du réseau d’assainissement.', 'voirie', 'urgente', 90, 5, 'nouvelle', NULL, '2026-05-18 13:20:12', 1),
(12, 'REC-2026-0011', 12, 'centre', 'Problème d’éclairage public', 'Depuis plusieurs jours, l’éclairage public de notre rue ne fonctionne plus correctement. La zone est très sombre durant la nuit, ce qui crée un sentiment d’insécurité pour les habitants et les passants. Nous vous remercions de bien vouloir intervenir afin de rétablir l’éclairage dans les meilleurs délais.', 'eclairage', 'moyenne', 50, 1, 'nouvelle', 'REC-2026-0011_prob eclairage.jfif', '2026-06-01 01:32:11', 0),
(13, 'REC-2026-0013', 13, 'centre', 'Problème d’éclairage public', 'Depuis plusieurs jours, l’éclairage public de notre rue ne fonctionne plus correctement. La zone est très sombre durant la nuit, ce qui crée un sentiment d’insécurité pour les habitants et les passants. Nous vous remercions de bien vouloir intervenir afin de rétablir l’éclairage dans les meilleurs délais.', 'eclairage', 'moyenne', 50, 1, 'nouvelle', 'REC-2026-0013_prob eclairage.jfif', '2026-06-01 01:33:35', 0),
(14, 'REC-2026-0014', 14, 'centre', 'Problème d’éclairage public', 'Depuis plusieurs jours, l’éclairage public de notre rue ne fonctionne plus correctement. La zone est très sombre durant la nuit, ce qui crée un sentiment d’insécurité pour les habitants et les passants. Nous vous remercions de bien vouloir intervenir afin de rétablir l’éclairage dans les meilleurs délais.', 'eclairage', 'moyenne', 50, 1, 'nouvelle', 'REC-2026-0014_prob eclairage.jfif', '2026-06-01 01:35:06', 0),
(15, 'REC-2026-0015', 15, 'وسط المدينة', 'انعدام الإنارة العمومية في الشارع', 'السلام عليكم،\r\nأود التبليغ عن مشكل في الإنارة العمومية بشارع رئيسي وسط المدينة. الشارع مظلم جداً بعد غروب الشمس بسبب تعطل عدة مصابيح منذ أكثر من أسبوع، مما يسبب خوفاً للسكان ويشكل خطراً على المارة، خصوصاً الأطفال والنساء خلال الليل.\r\nنرجو من المصالح المختصة التدخل في أقرب وقت لإصلاح المصابيح وإعادة الإنارة إلى الشارع.\r\nوشكراً.', 'eclairage', 'urgente', 90, 1, 'nouvelle', 'REC-2026-0015_انعدام الإنارة العمومية في الشارع.jfif', '2026-06-01 02:00:15', 0),
(16, 'REC-2026-0016', 16, 'birami', 'Poteau électrique menaçant de tomber', 'Depuis plusieurs jours, un poteau électrique situé à proximité de l’école primaire du quartier est fortement incliné et présente des fissures visibles à sa base. Les câbles sont également détendus et passent très près de la chaussée.\r\n\r\nCette situation représente un danger important pour les élèves, les passants et les véhicules. En cas de vent fort ou d’intempéries, le poteau risque de tomber et de provoquer un accident grave ou une coupure de courant dans tout le secteur.\r\n\r\nNous demandons une intervention urgente des services compétents afin de sécuriser la zone et remplacer le poteau défectueux.', 'voirie', 'urgente', 90, 3, 'nouvelle', NULL, '2026-06-01 03:57:00', 0),
(17, 'REC-2026-0017', 17, 'centre villr ', 'Panne de l\'éclairage public dans plusieurs rues du quartier', 'Depuis environ deux semaines, plusieurs lampadaires situés dans les rues principales du quartier Hay Salam ne fonctionnent plus. La zone est plongée dans l\'obscurité chaque nuit, ce qui crée un sentiment d\'insécurité pour les habitants, notamment les personnes âgées et les étudiants qui rentrent tard.\r\n\r\nLa situation a déjà provoqué plusieurs incidents mineurs, notamment des chutes de piétons à cause de la mauvaise visibilité. Le problème concerne principalement l\'avenue Hassan II et les rues adjacentes.\r\n\r\nNous demandons une intervention rapide des services compétents afin de réparer ou remplacer les équipements défectueux et rétablir l\'éclairage public dans les meilleurs délais.', 'eclairage', 'moyenne', 50, 1, 'nouvelle', 'REC-2026-0017_secure_compliance_architecture.png', '2026-06-02 11:13:42', 0),
(18, 'REC-2026-0018', 18, 'centre villr ', 'عطب في عمود الانارة', 'مصباح لايلااتعلعل', 'eclairage', 'faible', 30, 1, 'nouvelle', 'REC-2026-0018_secure_compliance_architecture.png', '2026-06-02 11:33:44', 0),
(19, 'REC-2026-0019', 19, 'centre', 'ماء كهرباء', 'ماء كهرباء', 'eau', 'faible', 30, 2, 'nouvelle', NULL, '2026-06-02 11:37:59', 0),
(20, 'REC-2026-0020', 20, 'Hay Riad', 'Panne d\'éclairage public dans la rue principale', 'Depuis environ deux semaines, plusieurs lampadaires situés dans la rue principale de Hay Riad, à proximité de l\'arrêt de bus et de l\'école du quartier, ne fonctionnent plus. Cette situation rend la circulation difficile la nuit et augmente le sentiment d\'insécurité pour les habitants. Nous sollicitons une intervention rapide afin de rétablir l\'éclairage public.', 'eclairage', 'urgente', 90, 1, 'cloturee', 'REC-2026-0020_eclairage.png', '2026-06-15 22:00:17', 0),
(21, 'REC-2026-0021', 21, 'Avenue Mohammed V', 'Lampadaire endommagé suite à l\'affaissement de la chaussée', 'Depuis plusieurs jours, un important affaissement de la chaussée est apparu sur l\'Avenue Mohammed V. Suite à cet affaissement, un lampadaire situé à proximité penche dangereusement et risque de tomber. La circulation des véhicules est perturbée et la zone est devenue dangereuse pour les piétons. Nous demandons une intervention rapide afin de sécuriser les lieux et réparer les équipements concernés.', 'voirie', 'urgente', 90, 3, 'nouvelle', NULL, '2026-06-16 00:49:10', 0),
(22, 'REC-2026-0022', 22, 'Hay Al Amal', 'Panne répétée des lampadaires près de la fontaine publique', 'Depuis plusieurs semaines, les lampadaires situés à proximité de la fontaine publique du quartier Hay Al Amal tombent régulièrement en panne. Certains restent éteints plusieurs jours avant d\'être rétablis. En observant la zone, nous avons constaté qu\'une importante fuite d\'eau est présente au pied des poteaux d\'éclairage et que l\'eau s\'accumule en permanence autour des installations électriques. Nous craignons que cette fuite soit à l\'origine des dysfonctionnements répétés de l\'éclairage public et représente également un danger pour les passants. Nous demandons une intervention rapide afin de résoudre ce problème.', 'eclairage', 'urgente', 90, 2, 'nouvelle', NULL, '2026-06-16 00:51:29', 1),
(23, 'REC-2026-0023', 23, 'حي الرياض', 'تعطل أعمدة الإنارة بالشارع الرئيسي', 'منذ أكثر من أسبوعين، لا تعمل عدة أعمدة إنارة في الشارع الرئيسي بحي الرياض بالقرب من محطة الحافلات والمدرسة الابتدائية. تسبب هذا الوضع في صعوبة التنقل ليلاً وزاد من شعور السكان بعدم الأمان. نرجو التدخل في أقرب وقت لإصلاح الأعطال وإعادة الإنارة العمومية.', 'eclairage', 'urgente', 90, 1, 'nouvelle', NULL, '2026-06-16 01:43:33', 0);

-- --------------------------------------------------------

--
-- Structure de la table `reponses`
--

CREATE TABLE `reponses` (
  `id` int(11) NOT NULL,
  `reclamation_id` int(11) NOT NULL,
  `utilisateur_id` int(11) DEFAULT NULL,
  `message` text DEFAULT NULL,
  `fichier_reponse` varchar(255) DEFAULT NULL,
  `date_reponse` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `reponses`
--

INSERT INTO `reponses` (`id`, `reclamation_id`, `utilisateur_id`, `message`, `fichier_reponse`, `date_reponse`) VALUES
(2, 5, NULL, 'Bonjour Madame,\r\n\r\nNous accusons réception de votre réclamation concernant le problème d’éclairage dans votre quartier situé à Birami.\r\n\r\nVotre demande a bien été prise en charge et transmise à la Division Éclairage Public pour intervention. Une équipe technique sera mobilisée afin de vérifier l’état des installations et procéder aux réparations nécessaires dans les plus brefs délais.\r\n\r\nNous vous remercions pour votre vigilance et votre contribution à l’amélioration des services publics.\r\n\r\nNous restons à votre disposition pour toute information complémentaire.\r\n\r\nCordialement,\r\nService Technique\r\nCommune', NULL, '2026-05-05 12:52:00'),
(3, 6, NULL, 'Bonjour Madame,\r\n\r\nNous accusons réception de votre réclamation concernant le problème d’éclairage public signalé dans votre quartier situé au centre-ville.\r\n\r\nVotre demande a bien été enregistrée sous le code REC-2026-0006 et transmise à la Division Éclairage Public pour évaluation et intervention. Une équipe technique sera chargée de vérifier l’état des installations concernées afin d’identifier l’origine de la panne et de procéder aux réparations nécessaires dans les meilleurs délais.\r\n\r\nNous comprenons l’importance de l’éclairage public pour la sécurité et le bien-être des habitants, et nous vous remercions pour votre vigilance ainsi que pour votre contribution à l’amélioration de votre cadre de vie.\r\n\r\nNous restons à votre disposition pour toute information complémentaire.\r\n\r\nCordialement,\r\nService Technique Communal\r\nDivision Éclairage Public', NULL, '2026-05-18 12:32:14'),
(4, 20, NULL, 'Madame, Monsieur,\r\n\r\nNous accusons réception de votre réclamation concernant la panne d’éclairage public signalée dans la rue principale du quartier Hay Riad, à proximité de l’arrêt de bus et de l’école.\r\n\r\nAprès examen de votre signalement, notre équipe technique a été informée de la situation et une intervention a été programmée dans les plus brefs délais afin d’identifier l’origine de la panne et de procéder aux réparations nécessaires.\r\n\r\nNous sommes conscients des désagréments et des risques liés à l’absence d’éclairage dans cette zone, notamment pour la sécurité des habitants et des usagers durant la nuit. Cette réclamation a donc été classée comme prioritaire et fera l’objet d’un suivi particulier jusqu’au rétablissement complet du service.\r\n\r\nNous vous remercions pour votre vigilance et votre contribution à l’amélioration du cadre de vie de notre commune.\r\n\r\nCordialement,\r\n\r\nDivision Éclairage Public\r\nCommune de Kénitra\r\n', NULL, '2026-06-16 00:47:09');

-- --------------------------------------------------------

--
-- Structure de la table `utilisateurs`
--

CREATE TABLE `utilisateurs` (
  `id` int(11) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `mot_de_passe` varchar(255) NOT NULL,
  `role` enum('admin','chef_division','agent') NOT NULL,
  `division_id` int(11) DEFAULT NULL,
  `doit_changer_mot_de_passe` tinyint(1) DEFAULT 1,
  `actif` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `utilisateurs`
--

INSERT INTO `utilisateurs` (`id`, `nom`, `email`, `mot_de_passe`, `role`, `division_id`, `doit_changer_mot_de_passe`, `actif`) VALUES
(2, 'Chef Division Éclairage Public', 'eclairagepublic@commune.ma', 'scrypt:32768:8:1$Jh5xNOEAFaxhOWN9$f8f2721b3decad858a2a65b5b0ea77b5d6d00e6f1087ba42e278306a34e1fb95b35d001c569610d5b0cd487396bdf9929357c1cdd92ea72e5979c33b4c9dcfe4', 'chef_division', 1, 0, 1),
(3, 'Chef Division Eau', 'eau@commune.ma', 'scrypt:32768:8:1$XisjQpE9R1bsRmk0$6af787e75d68a0c88588d504169e29cba0b822cea026d801fc73ab68442c809e423e5e0fd24ae3e253e2a48a827517794e92b7ce935a2b1ac0976ddc85632c7d', 'chef_division', 2, 0, 1),
(4, 'Chef Division Voirie', 'voirie@commune.ma', 'scrypt:32768:8:1$fbrBsOw7zdtlvY7l$ae6252b40a848916c32461a9fafe2794e28999e046715e3891a37c7b459ab28c18049ba4aa78083d11d923effb5d00614dd026b1c8b6d2b3382adaf6221e62ee', 'chef_division', 3, 1, 1),
(5, 'Chef Division Propreté', 'proprete@commune.ma', 'scrypt:32768:8:1$OKEfUfleelfq1hmC$6b8299fa26adc5823c70217d247f8a427478596d5a686908513ea64de9b68298b596732715e49193afbdf3a6d9c656cf124eb02c2aa5ce84949fbf528387e695', 'chef_division', 4, 0, 1),
(6, 'Chef Division Assainissement', 'assainissement@commune.ma', 'scrypt:32768:8:1$M3Ee1dDzwhfEB3s7$da955832249000876c77fe52779951fca84b7f0824aacaf5145de8e9661bc9241906a3b3234d5bf73dda8edb14b1e4f69ebe47dd6b9d57df9bafb3ed54b58658', 'chef_division', 5, 1, 1),
(7, 'Administrateur', 'admin@commune.ma', 'scrypt:32768:8:1$B7H35w3O7qS4RQre$e49356272f4bcecc732427a19f816f333c7245ce9b12ef08418c5f566c235928feb1aeb002b036f6f8a62de33e4d102c6f66798c63e9b87895485298eb51e525', 'admin', NULL, 0, 1),
(9, 'Division Éclairage Public 2', 'eclairagepublic2@commune.ma', 'scrypt:32768:8:1$bqeHVxFfLWIVbXUP$a2bd4bf906909fd6ca104de91d5355e5ebc44d6fa336fd454115a68dab904841b7cf03759bcdcedb040a9a59c069cdc565fc4f5709017f2f95869bfce7c8adfa', 'chef_division', 1, 1, 0);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `citoyens`
--
ALTER TABLE `citoyens`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `divisions`
--
ALTER TABLE `divisions`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `historique_reclamations`
--
ALTER TABLE `historique_reclamations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `reclamation_id` (`reclamation_id`),
  ADD KEY `utilisateur_id` (`utilisateur_id`);

--
-- Index pour la table `reclamations`
--
ALTER TABLE `reclamations`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code_reclamation` (`code_reclamation`),
  ADD KEY `citoyen_id` (`citoyen_id`),
  ADD KEY `division_id` (`division_id`);

--
-- Index pour la table `reponses`
--
ALTER TABLE `reponses`
  ADD PRIMARY KEY (`id`),
  ADD KEY `reclamation_id` (`reclamation_id`),
  ADD KEY `utilisateur_id` (`utilisateur_id`);

--
-- Index pour la table `utilisateurs`
--
ALTER TABLE `utilisateurs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `division_id` (`division_id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `citoyens`
--
ALTER TABLE `citoyens`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT pour la table `divisions`
--
ALTER TABLE `divisions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `historique_reclamations`
--
ALTER TABLE `historique_reclamations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT pour la table `reclamations`
--
ALTER TABLE `reclamations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT pour la table `reponses`
--
ALTER TABLE `reponses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `utilisateurs`
--
ALTER TABLE `utilisateurs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `historique_reclamations`
--
ALTER TABLE `historique_reclamations`
  ADD CONSTRAINT `historique_reclamations_ibfk_1` FOREIGN KEY (`reclamation_id`) REFERENCES `reclamations` (`id`),
  ADD CONSTRAINT `historique_reclamations_ibfk_2` FOREIGN KEY (`utilisateur_id`) REFERENCES `utilisateurs` (`id`);

--
-- Contraintes pour la table `reclamations`
--
ALTER TABLE `reclamations`
  ADD CONSTRAINT `reclamations_ibfk_1` FOREIGN KEY (`citoyen_id`) REFERENCES `citoyens` (`id`),
  ADD CONSTRAINT `reclamations_ibfk_2` FOREIGN KEY (`division_id`) REFERENCES `divisions` (`id`);

--
-- Contraintes pour la table `reponses`
--
ALTER TABLE `reponses`
  ADD CONSTRAINT `reponses_ibfk_1` FOREIGN KEY (`reclamation_id`) REFERENCES `reclamations` (`id`),
  ADD CONSTRAINT `reponses_ibfk_2` FOREIGN KEY (`utilisateur_id`) REFERENCES `utilisateurs` (`id`);

--
-- Contraintes pour la table `utilisateurs`
--
ALTER TABLE `utilisateurs`
  ADD CONSTRAINT `utilisateurs_ibfk_1` FOREIGN KEY (`division_id`) REFERENCES `divisions` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
