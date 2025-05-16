# Copyright (c) 2025, company to determine the Return on Investment (ROI) for clients switching to solar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime, now_datetime
from datetime import datetime
import calendar

class SolarCalculation(Document):
	def before_save(self):
		"""Set serial number and validate dates before saving"""
		if not self.serial_number:
			self.serial_number = self.generate_serial_number()
		self.validate_dates()

	def generate_serial_number(self):
		"""Generate serial number based on customer and counter"""
		count = frappe.db.count('Solar Calculation', {'customer': self.customer}) + 1
		return f"{self.customer}-{count:03d}"

	def validate_dates(self):
		"""Validate that end date is after start date"""
		if self.start_date and self.end_date:
			if get_datetime(self.end_date) < get_datetime(self.start_date):
				frappe.throw("End Date must be after Start Date")

	@frappe.whitelist()
	def calculate_averages(self):
		"""Calculate average KW, KWH and tariffs"""
		if not self.consumption_data:
			frappe.throw("No consumption data available")
			
		# Initialize variables
		total_kw = 0
		total_kwh = 0
		count = len(self.consumption_data)
		monthly_data = {}
		
		for record in self.consumption_data:
			total_kw += float(record.kw)
			total_kwh += float(record.kwh)
			
			# Get timestamp and month
			timestamp = get_datetime(record.timestamp)
			month = timestamp.strftime("%Y-%m")
			
			if month not in monthly_data:
				monthly_data[month] = {
					'low_tariff_kwh': [],
					'high_tariff_kwh': []
				}
			
			# Determine tariff period
			hour = timestamp.hour
			is_low_tariff = (hour >= 23 or hour < 6)
			
			if is_low_tariff:
				monthly_data[month]['low_tariff_kwh'].append(float(record.kwh))
			else:
				monthly_data[month]['high_tariff_kwh'].append(float(record.kwh))
		
		# Calculate averages
		self.average_kw = total_kw / count if count > 0 else 0
		self.average_kwh = total_kwh / count if count > 0 else 0
		
		# Clear existing tariffs
		self.monthly_tariffs = []
		
		# Calculate monthly tariffs
		for month, data in monthly_data.items():
			avg_low_kwh = sum(data['low_tariff_kwh']) / len(data['low_tariff_kwh']) if data['low_tariff_kwh'] else 0
			avg_high_kwh = sum(data['high_tariff_kwh']) / len(data['high_tariff_kwh']) if data['high_tariff_kwh'] else 0
			
			# Create child table entry
			self.append('monthly_tariffs', {
				'month': month,
				'low_tariff': 0.1 * avg_low_kwh,
				'high_tariff': 0.3 * avg_high_kwh
			})
		
		self.save()
		return self
