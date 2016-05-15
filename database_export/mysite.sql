-- phpMyAdmin SQL Dump
-- version 4.5.5.1
-- http://www.phpmyadmin.net
--
-- Client :  127.0.0.1
-- Généré le :  Dim 15 Mai 2016 à 12:17
-- Version du serveur :  5.7.11
-- Version de PHP :  5.6.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `mysite`
--

-- --------------------------------------------------------

--
-- Structure de la table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(80) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Contenu de la table `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(1, 'Artistes');

-- --------------------------------------------------------

--
-- Structure de la table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Contenu de la table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can add permission', 2, 'add_permission'),
(5, 'Can change permission', 2, 'change_permission'),
(6, 'Can delete permission', 2, 'delete_permission'),
(7, 'Can add group', 3, 'add_group'),
(8, 'Can change group', 3, 'change_group'),
(9, 'Can delete group', 3, 'delete_group'),
(10, 'Can add user', 4, 'add_user'),
(11, 'Can change user', 4, 'change_user'),
(12, 'Can delete user', 4, 'delete_user'),
(13, 'Can add content type', 5, 'add_contenttype'),
(14, 'Can change content type', 5, 'change_contenttype'),
(15, 'Can delete content type', 5, 'delete_contenttype'),
(16, 'Can add session', 6, 'add_session'),
(17, 'Can change session', 6, 'change_session'),
(18, 'Can delete session', 6, 'delete_session'),
(19, 'Can add site', 7, 'add_site'),
(20, 'Can change site', 7, 'change_site'),
(21, 'Can delete site', 7, 'delete_site'),
(35, 'Can change music', 12, 'change_music'),
(34, 'Can add music', 12, 'add_music'),
(33, 'Can delete tag', 11, 'delete_tag'),
(32, 'Can change tag', 11, 'change_tag'),
(31, 'Can add tag', 11, 'add_tag'),
(28, 'Can add registration', 10, 'add_registration'),
(29, 'Can change registration', 10, 'change_registration'),
(30, 'Can delete registration', 10, 'delete_registration'),
(36, 'Can delete music', 12, 'delete_music'),
(37, 'Can add album', 13, 'add_album'),
(38, 'Can change album', 13, 'change_album'),
(39, 'Can delete album', 13, 'delete_album');

-- --------------------------------------------------------

--
-- Structure de la table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Contenu de la table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(4, 'pbkdf2_sha256$24000$ybkT8sJqfry0$WZ5DIValYJIfe/phITNe/K1l3YTteuoaqAKQNF35K5s=', '2016-05-03 07:22:16.264000', 1, 'Admin', '', '', 'admin@site.com', 1, 1, '2016-05-02 18:03:18.169000'),
(22, 'pbkdf2_sha256$24000$L3rfEEM0bfn5$Fj2k5Bg/w+f0D7oKhU8DbBZ747L8H4wgncfqNqPvVDc=', NULL, 0, 'toto', '', '', 'test@test.fr', 0, 1, '2016-05-03 07:38:41.077000');

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Contenu de la table `auth_user_groups`
--

INSERT INTO `auth_user_groups` (`id`, `user_id`, `group_id`) VALUES
(1, 1, 1),
(18, 22, 1);

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Contenu de la table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2016-05-02 18:00:47.120000', '1', 'Artistes', 2, 'No fields changed.', 3, 3),
(2, '2016-05-02 18:07:06.437000', '5', 'toto', 3, '', 4, 4),
(3, '2016-05-02 18:09:53.907000', '1', 'Registration object', 3, '', 10, 4),
(4, '2016-05-02 18:10:11.546000', '6', 'toto', 3, '', 4, 4),
(5, '2016-05-02 18:14:28.960000', '7', 'toto', 3, '', 4, 4),
(6, '2016-05-02 18:18:17.643000', '8', 'toto', 3, '', 4, 4),
(7, '2016-05-02 18:50:02.387000', '9', 'toto', 3, '', 4, 4),
(8, '2016-05-02 18:52:12.561000', '10', 'toto', 3, '', 4, 4),
(9, '2016-05-02 19:07:51.646000', '11', 'toto', 3, '', 4, 4),
(10, '2016-05-02 19:22:17.726000', '12', 'toto', 3, '', 4, 4),
(11, '2016-05-02 19:40:53.150000', '13', 'toto', 3, '', 4, 4),
(12, '2016-05-02 19:44:04.368000', '14', 'toto', 3, '', 4, 4),
(13, '2016-05-02 19:47:41.294000', '15', 'toto', 3, '', 4, 4),
(14, '2016-05-02 19:50:19.423000', '16', 'toto', 3, '', 4, 4),
(15, '2016-05-02 20:10:24.511000', '17', 'toto', 3, '', 4, 4),
(16, '2016-05-02 22:07:25.505000', '18', 'toto', 3, '', 4, 4),
(17, '2016-05-02 22:23:08.705000', '19', 'toto', 3, '', 4, 4),
(18, '2016-05-02 22:57:33.562000', '20', 'toto', 3, '', 4, 4),
(19, '2016-05-03 07:28:19.618000', '21', 'toto', 3, '', 4, 4),
(20, '2016-05-04 17:01:40.721000', '1', 'Rock', 1, 'Ajout.', 11, 4),
(21, '2016-05-04 17:03:08.133000', '1', 'La terre est ronde de toto', 1, 'Ajout.', 13, 4),
(22, '2016-05-04 17:49:20.296000', '3', 'Je suis une musique de toto duree: 0:02:30', 2, 'Modification de path.', 12, 4),
(23, '2016-05-04 17:57:45.380000', '3', 'Je suis une musique de toto duree: 0:02:30', 3, '', 12, 4),
(24, '2016-05-04 18:05:03.263000', '4', 'Je suis une musique de toto duree: 0:02:30', 3, '', 12, 4),
(25, '2016-05-04 18:20:37.859000', '6', 'La terre est ronde 2 de toto duree: 0:02:30', 3, '', 12, 4),
(26, '2016-05-04 18:20:37.863000', '5', 'Je suis une musique de toto duree: 0:02:30', 3, '', 12, 4),
(27, '2016-05-04 18:57:58.354000', '7', 'Je suis une musique de toto duree: 0:02:30', 3, '', 12, 4),
(28, '2016-05-04 19:05:42.377000', '8', 'Je suis une musique de toto duree: 0:02:30', 3, '', 12, 4),
(29, '2016-05-04 19:10:05.484000', '9', 'Je suis une musique de toto duree: 0:02:30', 3, '', 12, 4),
(30, '2016-05-04 19:13:26.710000', '10', 'Je suis une musique de toto duree: 0:02:30', 3, '', 12, 4),
(31, '2016-05-04 19:25:04.879000', '12', 'La terre est ronde 2 de toto duree: 0:02:30', 3, '', 12, 4),
(32, '2016-05-04 19:25:04.882000', '11', 'Je suis une musique de toto duree: 0:02:30', 3, '', 12, 4),
(33, '2016-05-04 19:35:23.505000', '13', 'Je suis une musique de toto duree: 0:02:30', 3, '', 12, 4),
(34, '2016-05-04 19:38:19.762000', '14', 'Je suis une musique de toto duree: 0:02:30', 3, '', 12, 4),
(35, '2016-05-04 19:46:49.291000', '15', 'Je suis une musique de toto duree: 0:02:30', 3, '', 12, 4),
(36, '2016-05-06 08:38:46.839000', '16', 'Je suis une musique de toto duree: 0:02:30', 3, '', 12, 4);

-- --------------------------------------------------------

--
-- Structure de la table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Contenu de la table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(7, 'sites', 'site'),
(12, 'workspace', 'music'),
(11, 'workspace', 'tag'),
(10, 'workspace', 'registration'),
(13, 'workspace', 'album');

-- --------------------------------------------------------

--
-- Structure de la table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Contenu de la table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2016-05-02 09:43:30.504000'),
(2, 'auth', '0001_initial', '2016-05-02 09:43:32.950000'),
(3, 'admin', '0001_initial', '2016-05-02 09:43:33.434000'),
(4, 'admin', '0002_logentry_remove_auto_add', '2016-05-02 09:43:33.629000'),
(5, 'contenttypes', '0002_remove_content_type_name', '2016-05-02 09:43:33.895000'),
(6, 'auth', '0002_alter_permission_name_max_length', '2016-05-02 09:43:34.051000'),
(7, 'auth', '0003_alter_user_email_max_length', '2016-05-02 09:43:34.160000'),
(8, 'auth', '0004_alter_user_username_opts', '2016-05-02 09:43:34.207000'),
(9, 'auth', '0005_alter_user_last_login_null', '2016-05-02 09:43:34.317000'),
(10, 'auth', '0006_require_contenttypes_0002', '2016-05-02 09:43:34.332000'),
(11, 'auth', '0007_alter_validators_add_error_messages', '2016-05-02 09:43:34.379000'),
(12, 'sessions', '0001_initial', '2016-05-02 09:43:34.613000'),
(13, 'sites', '0001_initial', '2016-05-02 09:43:34.723000'),
(14, 'sites', '0002_alter_domain_unique', '2016-05-02 09:43:34.832000'),
(15, 'workspace', '0001_initial', '2016-05-02 09:43:35.153000'),
(16, 'workspace', '0002_auto_20160501_2138', '2016-05-02 09:43:35.638000'),
(17, 'workspace', '0003_auto_20160501_2139', '2016-05-02 09:43:35.763000'),
(18, 'workspace', '0004_auto_20160502_1935', '2016-05-02 17:36:11.662000'),
(19, 'workspace', '0005_auto_20160503_1032', '2016-05-03 08:32:59.982000'),
(20, 'workspace', '0006_music_auteur', '2016-05-03 13:07:56.040000'),
(21, 'workspace', '0007_auto_20160503_1508', '2016-05-03 13:08:22.319000'),
(22, 'workspace', '0008_auto_20160503_1625', '2016-05-03 14:25:11.718000'),
(23, 'workspace', '0009_auto_20160504_1654', '2016-05-04 14:56:08.880000'),
(24, 'workspace', '0010_auto_20160504_2103', '2016-05-04 19:05:09.804000'),
(25, 'workspace', '0011_auto_20160504_2108', '2016-05-04 19:08:55.888000'),
(26, 'workspace', '0012_auto_20160504_2111', '2016-05-04 19:11:33.141000'),
(27, 'workspace', '0013_auto_20160504_2133', '2016-05-04 19:34:01.962000');

-- --------------------------------------------------------

--
-- Structure de la table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Contenu de la table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('135l5gvl15rc1tiyx3q91ephwjjv2c20', 'YjA4NTQwNGY1MGVhODFkYzFkMzI4NjYxMmRkYTMzYmEzMGExOTcwMzp7Il9hdXRoX3VzZXJfaGFzaCI6IjY1YjBjZDgyOGUwNTk0NzllYzdjYzY5NGY2OTM0Y2UzMWJhNWM2NGYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiI0In0=', '2016-05-17 07:22:16.268000');

-- --------------------------------------------------------

--
-- Structure de la table `django_site`
--

CREATE TABLE `django_site` (
  `id` int(11) NOT NULL,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Contenu de la table `django_site`
--

INSERT INTO `django_site` (`id`, `domain`, `name`) VALUES
(2, 'example.com', 'example.com');

-- --------------------------------------------------------

--
-- Structure de la table `workspace_album`
--

CREATE TABLE `workspace_album` (
  `id` int(11) NOT NULL,
  `titre` varchar(100) NOT NULL,
  `date_publication` date NOT NULL,
  `type_album` varchar(2) NOT NULL,
  `artiste_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Contenu de la table `workspace_album`
--

INSERT INTO `workspace_album` (`id`, `titre`, `date_publication`, `type_album`, `artiste_id`) VALUES
(1, 'La terre est ronde', '2016-05-04', 'AL', 22);

-- --------------------------------------------------------

--
-- Structure de la table `workspace_music`
--

CREATE TABLE `workspace_music` (
  `id` int(11) NOT NULL,
  `titre` varchar(100) NOT NULL,
  `duree` bigint(20) NOT NULL,
  `path` varchar(100) NOT NULL,
  `album_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  `auteur_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Contenu de la table `workspace_music`
--

INSERT INTO `workspace_music` (`id`, `titre`, `duree`, `path`, `album_id`, `tag_id`, `auteur_id`) VALUES
(17, 'Balanced Boy', 210000000, 'toto/La terre est ronde/4-5-2016/Millencolin_-_Balanced_Boy_Full_Album_Stream.mp3', 1, 1, 22);

-- --------------------------------------------------------

--
-- Structure de la table `workspace_registration`
--

CREATE TABLE `workspace_registration` (
  `id` int(11) NOT NULL,
  `key` varchar(100) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `workspace_tag`
--

CREATE TABLE `workspace_tag` (
  `id` int(11) NOT NULL,
  `intitule` varchar(100) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Contenu de la table `workspace_tag`
--

INSERT INTO `workspace_tag` (`id`, `intitule`) VALUES
(1, 'Rock');

--
-- Index pour les tables exportées
--

--
-- Index pour la table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Index pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissions_0e939a4f` (`group_id`),
  ADD KEY `auth_group_permissions_8373b171` (`permission_id`);

--
-- Index pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`),
  ADD KEY `auth_permission_417f1b1c` (`content_type_id`);

--
-- Index pour la table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Index pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_e8701ad4` (`user_id`),
  ADD KEY `auth_user_groups_0e939a4f` (`group_id`);

--
-- Index pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permissions_e8701ad4` (`user_id`),
  ADD KEY `auth_user_user_permissions_8373b171` (`permission_id`);

--
-- Index pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_417f1b1c` (`content_type_id`),
  ADD KEY `django_admin_log_e8701ad4` (`user_id`);

--
-- Index pour la table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Index pour la table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_de54fa62` (`expire_date`);

--
-- Index pour la table `django_site`
--
ALTER TABLE `django_site`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_site_domain_a2e37b91_uniq` (`domain`);

--
-- Index pour la table `workspace_album`
--
ALTER TABLE `workspace_album`
  ADD PRIMARY KEY (`id`),
  ADD KEY `workspace_album_24fa59d8` (`artiste_id`);

--
-- Index pour la table `workspace_music`
--
ALTER TABLE `workspace_music`
  ADD PRIMARY KEY (`id`),
  ADD KEY `workspace_music_95c3b9df` (`album_id`),
  ADD KEY `workspace_music_76f094bc` (`tag_id`),
  ADD KEY `workspace_music_2cc46b4c` (`auteur_id`);

--
-- Index pour la table `workspace_registration`
--
ALTER TABLE `workspace_registration`
  ADD PRIMARY KEY (`id`),
  ADD KEY `workspace_registration_e8701ad4` (`user_id`);

--
-- Index pour la table `workspace_tag`
--
ALTER TABLE `workspace_tag`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;
--
-- AUTO_INCREMENT pour la table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;
--
-- AUTO_INCREMENT pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;
--
-- AUTO_INCREMENT pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;
--
-- AUTO_INCREMENT pour la table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
--
-- AUTO_INCREMENT pour la table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;
--
-- AUTO_INCREMENT pour la table `django_site`
--
ALTER TABLE `django_site`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT pour la table `workspace_album`
--
ALTER TABLE `workspace_album`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT pour la table `workspace_music`
--
ALTER TABLE `workspace_music`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
--
-- AUTO_INCREMENT pour la table `workspace_registration`
--
ALTER TABLE `workspace_registration`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
--
-- AUTO_INCREMENT pour la table `workspace_tag`
--
ALTER TABLE `workspace_tag`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
