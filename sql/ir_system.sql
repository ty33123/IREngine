/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80012
 Source Host           : localhost:3306
 Source Schema         : ir_system

 Target Server Type    : MySQL
 Target Server Version : 80012
 File Encoding         : 65001

 Date: 02/01/2021 06:20:47
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for err_log
-- ----------------------------
DROP TABLE IF EXISTS `err_log`;
CREATE TABLE `err_log`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `err_msg` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '错误日志',
  `err_time` datetime(0) NULL DEFAULT NULL COMMENT '报错时间',
  `spider_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '爬虫名',
  `spider_file` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '爬虫文件',
  `spider_id` int(11) NULL DEFAULT NULL COMMENT '爬虫id',
  `is_fix` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '是否修复',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 331 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for news_data
-- ----------------------------
DROP TABLE IF EXISTS `news_data`;
CREATE TABLE `news_data`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '新闻url',
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '新闻标题',
  `content` text CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '新闻正文',
  `source` varchar(10) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '新闻采集源',
  `collect_time` datetime(0) NOT NULL COMMENT '爬虫采集时间',
  `publish_time` datetime(0) NOT NULL COMMENT '新闻发布时间',
  `read_counts` int(11) NOT NULL DEFAULT 0 COMMENT '阅读量',
  PRIMARY KEY (`id`, `url`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 69472 CHARACTER SET = utf8 COLLATE = utf8_bin ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for search_history
-- ----------------------------
DROP TABLE IF EXISTS `search_history`;
CREATE TABLE `search_history`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `search_word` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '用户检索词',
  `search_word2id` varchar(512) CHARACTER SET utf8 COLLATE utf8_bin NULL DEFAULT NULL COMMENT '检索词编码',
  `search_time` datetime(0) NOT NULL COMMENT '用户检索时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 49019 CHARACTER SET = utf8 COLLATE = utf8_bin ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for spider_list
-- ----------------------------
DROP TABLE IF EXISTS `spider_list`;
CREATE TABLE `spider_list`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '爬虫名称',
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '描述',
  `type` tinyint(1) NULL DEFAULT NULL COMMENT '爬虫启动时间间隔类型0定时1循环',
  `params` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '启动参数',
  `last_acq_num` int(11) NULL DEFAULT NULL COMMENT '上次爬取量',
  `acq_num` int(11) NULL DEFAULT NULL COMMENT '爬取总量',
  `is_error` tinyint(1) NULL DEFAULT NULL COMMENT '是否异常',
  `last_run_time` datetime(0) NULL DEFAULT NULL COMMENT '上次启动时间',
  `next_run_time` datetime(0) NULL DEFAULT NULL COMMENT '下次启动时间',
  `enabled` tinyint(1) NULL DEFAULT NULL COMMENT '是否启用',
  `file_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '文件名',
  `url` varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '公文列表页链接',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
