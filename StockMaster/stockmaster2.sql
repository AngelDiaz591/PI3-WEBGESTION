-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-02-2024 a las 20:05:26
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `stockmaster2`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add productos', 7, 'add_productos'),
(26, 'Can change productos', 7, 'change_productos'),
(27, 'Can delete productos', 7, 'delete_productos'),
(28, 'Can view productos', 7, 'view_productos'),
(29, 'Can add mensajes', 8, 'add_mensajes'),
(30, 'Can change mensajes', 8, 'change_mensajes'),
(31, 'Can delete mensajes', 8, 'delete_mensajes'),
(32, 'Can view mensajes', 8, 'view_mensajes'),
(33, 'Can add categoria', 9, 'add_categoria'),
(34, 'Can change categoria', 9, 'change_categoria'),
(35, 'Can delete categoria', 9, 'delete_categoria'),
(36, 'Can view categoria', 9, 'view_categoria'),
(37, 'Can add log', 10, 'add_log'),
(38, 'Can change log', 10, 'change_log'),
(39, 'Can delete log', 10, 'delete_log'),
(40, 'Can view log', 10, 'view_log'),
(41, 'Can add profile', 11, 'add_profile'),
(42, 'Can change profile', 11, 'change_profile'),
(43, 'Can delete profile', 11, 'delete_profile'),
(44, 'Can view profile', 11, 'view_profile');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$260000$GUM8NVe2batMGMGG4vhXpA$jiEykBcR2liKUnKhkYbzbRyAi3nnLxf1bO+gc5bO3aM=', '2023-11-21 06:42:38.589932', 1, 'ismael710', '', '', 'imontiel@ucol.mc', 1, 1, '2023-11-21 06:09:20.895510'),
(2, 'pbkdf2_sha256$260000$iUJwxxVAwszCDg6iKyPCfJ$rz1nIdJNvZkQcMrcmb818Rw0a1MpbG7fh2h9uPuA9FY=', NULL, 0, 'ismael11', 'ISMAEL', 'MONTIEL TORRES', 'mayelomonti1@gmail.com', 0, 1, '2023-11-21 06:43:08.134320');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2023-11-21 06:11:11.104602', '1', 'profile of ismael710', 2, '[{\"changed\": {\"fields\": [\"Bio\"]}}]', 11, 1),
(2, '2023-11-21 06:16:49.960320', '1', 'profile of ismael710', 2, '[{\"changed\": {\"fields\": [\"Photo\"]}}]', 11, 1),
(3, '2023-11-21 06:16:51.203191', '1', 'profile of ismael710', 2, '[]', 11, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(10, 'logs', 'log'),
(11, 'profiles', 'profile'),
(6, 'sessions', 'session'),
(9, 'StockMaster_app', 'categoria'),
(8, 'StockMaster_app', 'mensajes'),
(7, 'StockMaster_app', 'productos');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2023-11-21 06:07:21.190978'),
(2, 'auth', '0001_initial', '2023-11-21 06:07:22.167678'),
(3, 'StockMaster_app', '0001_initial', '2023-11-21 06:07:22.305576'),
(4, 'StockMaster_app', '0002_delete_customuser', '2023-11-21 06:07:22.325375'),
(5, 'StockMaster_app', '0003_initial', '2023-11-21 06:07:22.371597'),
(6, 'StockMaster_app', '0004_mensajes', '2023-11-21 06:07:22.418871'),
(7, 'StockMaster_app', '0005_rename_nusuario_mensajes_username', '2023-11-21 06:07:22.445680'),
(8, 'StockMaster_app', '0006_alter_mensajes_username', '2023-11-21 06:07:22.515769'),
(9, 'StockMaster_app', '0007_alter_mensajes_username', '2023-11-21 06:07:22.730598'),
(10, 'StockMaster_app', '0008_alter_mensajes_username', '2023-11-21 06:07:22.934238'),
(11, 'StockMaster_app', '0009_mensajes_tiempo_creacion', '2023-11-21 06:07:22.978812'),
(12, 'StockMaster_app', '0010_mensajes_respuestascomentarios', '2023-11-21 06:07:23.011055'),
(13, 'StockMaster_app', '0011_categoria', '2023-11-21 06:07:23.045758'),
(14, 'StockMaster_app', '0012_productos_id_categorias', '2023-11-21 06:07:23.145138'),
(15, 'StockMaster_app', '0013_alter_productos_id_categorias', '2023-11-21 06:07:23.297435'),
(16, 'StockMaster_app', '0014_productos_hora_baja_productos_status', '2023-11-21 06:07:23.364529'),
(17, 'StockMaster_app', '0015_productos_username', '2023-11-21 06:07:23.388375'),
(18, 'StockMaster_app', '0016_alter_productos_hora_baja', '2023-11-21 06:07:23.459913'),
(19, 'StockMaster_app', '0017_productos_usernamere', '2023-11-21 06:07:23.486865'),
(20, 'StockMaster_app', '0018_productos_fecha_edit', '2023-11-21 06:07:23.525655'),
(21, 'StockMaster_app', '0019_productos_useredit', '2023-11-21 06:07:23.552032'),
(22, 'StockMaster_app', '0020_productos_movimiento', '2023-11-21 06:07:23.603286'),
(23, 'admin', '0001_initial', '2023-11-21 06:07:23.803679'),
(24, 'admin', '0002_logentry_remove_auto_add', '2023-11-21 06:07:23.817317'),
(25, 'admin', '0003_logentry_add_action_flag_choices', '2023-11-21 06:07:23.832030'),
(26, 'contenttypes', '0002_remove_content_type_name', '2023-11-21 06:07:23.925358'),
(27, 'auth', '0002_alter_permission_name_max_length', '2023-11-21 06:07:24.007917'),
(28, 'auth', '0003_alter_user_email_max_length', '2023-11-21 06:07:24.040883'),
(29, 'auth', '0004_alter_user_username_opts', '2023-11-21 06:07:24.054365'),
(30, 'auth', '0005_alter_user_last_login_null', '2023-11-21 06:07:24.116344'),
(31, 'auth', '0006_require_contenttypes_0002', '2023-11-21 06:07:24.123105'),
(32, 'auth', '0007_alter_validators_add_error_messages', '2023-11-21 06:07:24.136710'),
(33, 'auth', '0008_alter_user_username_max_length', '2023-11-21 06:07:24.162837'),
(34, 'auth', '0009_alter_user_last_name_max_length', '2023-11-21 06:07:24.189837'),
(35, 'auth', '0010_alter_group_name_max_length', '2023-11-21 06:07:24.216673'),
(36, 'auth', '0011_update_proxy_permissions', '2023-11-21 06:07:24.231189'),
(37, 'auth', '0012_alter_user_first_name_max_length', '2023-11-21 06:07:24.260670'),
(38, 'profiles', '0001_initial', '2023-11-21 06:07:24.383646'),
(39, 'logs', '0001_initial', '2023-11-21 06:07:24.487091'),
(40, 'logs', '0002_rename_foto_log_photo_alter_log_profile', '2023-11-21 06:07:24.735911'),
(41, 'profiles', '0002_remove_profile_foto_profile_photo', '2023-11-21 06:07:24.800356'),
(42, 'sessions', '0001_initial', '2023-11-21 06:07:24.851910');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `logs_log`
--

CREATE TABLE `logs_log` (
  `id` bigint(20) NOT NULL,
  `photo` varchar(100) NOT NULL,
  `is_correct` tinyint(1) NOT NULL,
  `created` datetime(6) NOT NULL,
  `profile_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `logs_log`
--

INSERT INTO `logs_log` (`id`, `photo`, `is_correct`, `created`, `profile_id`) VALUES
(1, 'logs/upload_ZYqKD8T.png', 0, '2023-11-21 06:11:26.838376', NULL),
(2, 'logs/upload_FiRJLul.png', 0, '2023-11-21 06:11:50.289327', NULL),
(3, 'logs/upload_YbHl2jF.png', 0, '2023-11-21 06:14:00.631133', NULL),
(4, 'logs/upload_mlUyCYS.png', 0, '2023-11-21 06:17:07.106244', 1),
(5, 'logs/upload_zvEhbbA.png', 0, '2023-11-21 06:17:19.540615', 1),
(6, 'logs/upload_01HvHtb.png', 0, '2023-11-21 06:17:28.847430', NULL),
(7, 'logs/upload_iFyj2rN.png', 0, '2023-11-21 06:17:49.332537', NULL),
(8, 'logs/upload_CbtBAKX.png', 0, '2023-11-21 06:18:10.407625', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `profiles_profile`
--

CREATE TABLE `profiles_profile` (
  `id` bigint(20) NOT NULL,
  `bio` longtext NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  `photo` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `profiles_profile`
--

INSERT INTO `profiles_profile` (`id`, `bio`, `created`, `user_id`, `photo`) VALUES
(1, 'holapp', '2023-11-21 06:09:21.082011', 1, 'photos/WIN_20231121_00_10_52_Pro.jpg'),
(2, '', '2023-11-21 06:43:08.425049', 2, '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `stockmaster_app_categoria`
--

CREATE TABLE `stockmaster_app_categoria` (
  `categoria_id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `stockmaster_app_mensajes`
--

CREATE TABLE `stockmaster_app_mensajes` (
  `idcomentario` int(11) NOT NULL,
  `comentario` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `tiempo_creacion` datetime(6) NOT NULL,
  `respuestascomentarios` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `stockmaster_app_productos`
--

CREATE TABLE `stockmaster_app_productos` (
  `idproducts` int(11) NOT NULL,
  `codigo` varchar(255) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `precio` bigint(20) UNSIGNED NOT NULL CHECK (`precio` >= 0),
  `marca` varchar(255) NOT NULL,
  `cantPro` varchar(255) NOT NULL,
  `imagen` longblob DEFAULT NULL,
  `id_categorias_id` int(11) NOT NULL,
  `hora_baja` datetime(6) DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `usernamere` varchar(255) DEFAULT NULL,
  `fecha_edit` datetime(6) DEFAULT NULL,
  `useredit` varchar(255) DEFAULT NULL,
  `movimiento` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `logs_log`
--
ALTER TABLE `logs_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `logs_log_profile_id_41ff81c7_fk_profiles_profile_id` (`profile_id`);

--
-- Indices de la tabla `profiles_profile`
--
ALTER TABLE `profiles_profile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indices de la tabla `stockmaster_app_categoria`
--
ALTER TABLE `stockmaster_app_categoria`
  ADD PRIMARY KEY (`categoria_id`);

--
-- Indices de la tabla `stockmaster_app_mensajes`
--
ALTER TABLE `stockmaster_app_mensajes`
  ADD PRIMARY KEY (`idcomentario`);

--
-- Indices de la tabla `stockmaster_app_productos`
--
ALTER TABLE `stockmaster_app_productos`
  ADD PRIMARY KEY (`idproducts`),
  ADD KEY `StockMaster_app_prod_id_categorias_id_777a1990_fk_StockMast` (`id_categorias_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT de la tabla `logs_log`
--
ALTER TABLE `logs_log`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `profiles_profile`
--
ALTER TABLE `profiles_profile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `stockmaster_app_categoria`
--
ALTER TABLE `stockmaster_app_categoria`
  MODIFY `categoria_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `stockmaster_app_mensajes`
--
ALTER TABLE `stockmaster_app_mensajes`
  MODIFY `idcomentario` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `stockmaster_app_productos`
--
ALTER TABLE `stockmaster_app_productos`
  MODIFY `idproducts` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `logs_log`
--
ALTER TABLE `logs_log`
  ADD CONSTRAINT `logs_log_profile_id_41ff81c7_fk_profiles_profile_id` FOREIGN KEY (`profile_id`) REFERENCES `profiles_profile` (`id`);

--
-- Filtros para la tabla `profiles_profile`
--
ALTER TABLE `profiles_profile`
  ADD CONSTRAINT `profiles_profile_user_id_a3e81f91_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `stockmaster_app_productos`
--
ALTER TABLE `stockmaster_app_productos`
  ADD CONSTRAINT `StockMaster_app_prod_id_categorias_id_777a1990_fk_StockMast` FOREIGN KEY (`id_categorias_id`) REFERENCES `stockmaster_app_categoria` (`categoria_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
