# -*- coding: utf-8 -*-
##############################################################################
# @@@LICENSE
#
# Copyright(c) 2018 by LG Electronics Inc.
#
#   Confidential computer software. Valid license from LG Electronics required
#   for possession, use or copying. Consistent with FAR 12.211 and 12.212,
#   Commercial Computer Software, Computer Software Documentation, and
#   Technical Data for Commercial Items are licensed to the U.S. Government
#   under vendor's standard commercial license.
#
# LICENSE@@@
##############################################################################
#   VIN-020 (추후엔 제퍼id) ADC Calibration 동작
#   =================
#
#   DESCRIPTION :
#    (1) 1. press ADJ
#        2. choose [9. ADC Calibration"
#        3. choose ADC Type 1) OTP -> Start 2) Internal -> Start 3) External
#        4. press Start
#    (2) 1. Check whether there is any transient phenomenon happening after conducting ADC Calibration
#        2. Check [OK] after conducting ADC Calibration
#
##############################################################################

from webos.utils.pytell.input_generator_service import InputGeneratorService
from webos.tests_base.BaseTest import BaseTest
from webos.tests_base.BaseRetryTest import BaseRetryTest
from webos.utils.pytell.remote import Remote
import time


class Class4test(BaseTest):
	def __init__(self):
		test_name = "ADC Calibration 동작"
		BaseTest.__init__(self, test_name, author='sangwoo.ahn', connection_timeout_seconds=20.0)
		self.enable_addon(BaseRetryTest.ENABLE_PYTELL_ADDON)
		self.enable_addon(BaseRetryTest.APPS_GUARD_ADDON,
		                  ignore_after="com.webos.app.livetv")

	def run(self):
		try:
			# 1. Remote 생성
			mrcu = Remote(InputGeneratorService(self.get_command_line()))
			self.assertIsNotNone(mrcu, 'Creating mrcu instance [FAIL]')

			# 2. ADJ 진입
			self.log_info("Enter Adj menu.")
			mrcu.press_key('adj')
			time.sleep(3)
			for i in ['0','4','1','3']:
				mrcu.press_key(i)
				time.sleep(1)

			# 3. ADC Calibration 메뉴 진입입
			self.log_info("Go to ADC Calibration menu")
			for i in range(0,9):
				mrcu.press_key('down')
				time.sleep(1)
			mrcu.press_key('enter')
			time.sleep(1)

			# 4. OTP start
			self.log_info("Start OTP calibration")
			for key in ['down', 'enter']:
				mrcu.press_key(key)
				time.sleep(1)

			# 5. Internal start
			self.log_info("Start Internal calibration")
			for key in ['up', 'right','down','enter']:
				mrcu.press_key(key)
				time.sleep(1)

			# 결과 판단 코드 추가 필요.
			self.assertTrue(True, str('error'))
		except RuntimeError as error:
			self.assertFalse(True, str(error))
		finally:
			self.log_info("Close ADC Calibration Test")
