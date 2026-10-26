"""Safe, repeatable demo seeder for Smart E-Waste Recovery and Reuse Management System.

Populates fictional devices, components across 8 categories in all 3 test states,
admin & student accounts, requests, reuse transactions, and QR code assets.
Idempotent: Repeated execution will not duplicate records.
"""

from datetime import datetime, date, timedelta
from app import create_app
from app.extensions import db
from app.models import (
    User,
    Device,
    ComponentType,
    Component,
    ComponentTest,
    ComponentRequest,
    StockTransaction,
    AuditLog,
)
from app.services.qr_service import generate_component_qr

app = create_app()


def seed_database():
    with app.app_context():
        print("--- Seeding Smart E-Waste Database ---")

        # 1. Component Types (Seed if empty)
        type_definitions = [
            ("Resistor", "passive", "Fixed, precision, and variable resistors"),
            ("Capacitor", "passive", "Electrolytic, ceramic, and film capacitors"),
            ("Diode", "active", "Rectifier, Zener, Schottky, and indicator LEDs"),
            ("Transistor", "active", "BJT, MOSFET, and Darlington power semiconductors"),
            ("Integrated Circuit", "ic", "Timers, op-amps, regulators, and logic MCUs"),
            ("Relay", "electromechanical", "Electromechanical switches and PCB relays"),
            ("Connector", "electromechanical", "Headers, terminal blocks, jacks, and sockets"),
            ("Sensor", "module", "Temperature, light, and motion transducer modules"),
            ("Display", "module", "Seven-segment, LCD, and alphanumeric displays"),
            ("Other", "other", "Miscellaneous recovered electronic hardware"),
        ]

        types_map = {}
        for name, family, desc in type_definitions:
            ctype = ComponentType.query.filter_by(name=name).first()
            if not ctype:
                ctype = ComponentType(name=name, family=family, description=desc)
                db.session.add(ctype)
                db.session.flush()
            types_map[name] = ctype
        db.session.commit()
        print(f"[OK] Component types verified ({len(types_map)} types)")

        # 2. Demo Users
        users_to_seed = [
            {
                "full_name": "Dr. Sarah Admin",
                "username": "admin",
                "email": "admin@ewaste.edu",
                "password": "Admin@123",
                "role": "admin",
            },
            {
                "full_name": "Alex Student",
                "username": "alexa",
                "email": "student@ewaste.edu",
                "password": "Student@123",
                "role": "student",
            },
            {
                "full_name": "Rohan Patel",
                "username": "rohan",
                "email": "rohan.ece@ewaste.edu",
                "password": "Student@123",
                "role": "student",
            },
        ]

        users_map = {}
        for udata in users_to_seed:
            user = User.query.filter_by(email=udata["email"]).first()
            if not user:
                user = User(
                    full_name=udata["full_name"],
                    username=udata["username"],
                    email=udata["email"],
                    role=udata["role"],
                    is_active=True,
                    created_at=datetime.utcnow() - timedelta(days=30),
                )
                user.set_password(udata["password"])
                db.session.add(user)
                db.session.flush()
                print(f"Created demo user: {user.email} (Role: {user.role})")
            users_map[udata["email"]] = user
        db.session.commit()

        admin_user = users_map["admin@ewaste.edu"]
        student_user = users_map["student@ewaste.edu"]
        student_rohan = users_map["rohan.ece@ewaste.edu"]

        # 3. Fictional E-Waste Devices
        devices_to_seed = [
            {
                "code": "DEV-2026-0001",
                "name": "Dell OptiPlex 780 Desktop Tower",
                "category": "Computer / IT Hardware",
                "brand": "Dell",
                "model": "OptiPlex 780",
                "source": "Campus Computer Center Lab 2",
                "condition_notes": "Decommissioned PC with operational motherboard and ATX power supply.",
                "status": "dismantled",
                "received_date": date.today() - timedelta(days=25),
            },
            {
                "code": "DEV-2026-0002",
                "name": "HP LaserJet Pro 400 High Voltage Supply",
                "category": "Power Supplies & Adapters",
                "brand": "HP",
                "model": "M401dne",
                "source": "Department Administration Office",
                "condition_notes": "Paper feed failure; high-grade passive filtering stage intact.",
                "status": "dismantled",
                "received_date": date.today() - timedelta(days=20),
            },
            {
                "code": "DEV-2026-0003",
                "name": "Tektronix 2213 Analog Oscilloscope Chassis",
                "category": "Laboratory Instrumentation",
                "brand": "Tektronix",
                "model": "2213-60MHz",
                "source": "ECE Hardware Electronics Lab 3",
                "condition_notes": "CRT phosphor faded; discrete transistors and precision op-amps desoldered cleanly.",
                "status": "dismantling",
                "received_date": date.today() - timedelta(days=15),
            },
            {
                "code": "DEV-2026-0004",
                "name": "Sony Bravia 32-inch LCD TV Mainboard",
                "category": "Consumer Electronics",
                "brand": "Sony",
                "model": "KLV-32BX300",
                "source": "Hostel E-Waste Donation Drive",
                "condition_notes": "Cracked display panel; intact linear regulators, LEDs, and audio amplifier ICs.",
                "status": "received",
                "received_date": date.today() - timedelta(days=8),
            },
        ]

        devices_map = {}
        for ddata in devices_to_seed:
            dev = Device.query.filter_by(device_code=ddata["code"]).first()
            if not dev:
                dev = Device(
                    device_code=ddata["code"],
                    name=ddata["name"],
                    category=ddata["category"],
                    brand=ddata["brand"],
                    model=ddata["model"],
                    source=ddata["source"],
                    condition_notes=ddata["condition_notes"],
                    status=ddata["status"],
                    received_date=ddata["received_date"],
                    added_by=admin_user.id,
                    created_at=datetime.utcnow() - timedelta(days=20),
                )
                db.session.add(dev)
                db.session.flush()
                print(f"Created device: {dev.device_code} - {dev.name}")
            devices_map[ddata["code"]] = dev
        db.session.commit()

        # 4. Electronic Components Across All 8 Categories
        components_to_seed = [
            # Resistors
            {
                "code": "CMP-2026-0101",
                "device_code": "DEV-2026-0001",
                "type": "Resistor",
                "name": "Precision 10k Ohm Metal Film Resistor",
                "part_number": "MF-10K",
                "spec": "10k Ohm 1/4W 1% Precision Metal Film",
                "rated_value": "10k Ohm",
                "pkg": "Axial Through-Hole",
                "qty": 50,
                "location": "Cabinet R - Drawer 1 - Bin 10K",
                "state": "Reusable",  # tested pass
                "test_method": "Fluke 87V 4-Wire Resistance Test",
                "exp_val": 10000.0,
                "meas_val": 9980.0,
                "unit": "Ohm",
                "tol": 1.0,
            },
            {
                "code": "CMP-2026-0102",
                "device_code": "DEV-2026-0001",
                "type": "Resistor",
                "name": "220 Ohm LED Current Limiting Resistor",
                "part_number": "CF-220R",
                "spec": "220 Ohm 1/2W 5% Carbon Film",
                "rated_value": "220 Ohm",
                "pkg": "Axial Through-Hole",
                "qty": 40,
                "location": "Cabinet R - Drawer 1 - Bin 220",
                "state": "Reusable",  # tested pass
                "test_method": "Digital Multimeter Resistance Check",
                "exp_val": 220.0,
                "meas_val": 218.5,
                "unit": "Ohm",
                "tol": 5.0,
            },
            {
                "code": "CMP-2026-0103",
                "device_code": "DEV-2026-0002",
                "type": "Resistor",
                "name": "4.7k Ohm Pull-Up Resistor",
                "part_number": "CF-4K7",
                "spec": "4.7k Ohm 1/4W 5% Carbon Film",
                "rated_value": "4.7k Ohm",
                "pkg": "Axial Through-Hole",
                "qty": 30,
                "location": "Cabinet R - Drawer 2 - Bin 4K7",
                "state": "Needs Testing",  # untested
            },
            # Capacitors
            {
                "code": "CMP-2026-0201",
                "device_code": "DEV-2026-0002",
                "type": "Capacitor",
                "name": "100uF 25V Low-ESR Electrolytic Capacitor",
                "part_number": "EEU-FC1E101",
                "spec": "100uF 25V 105C Radial Electrolytic",
                "rated_value": "100uF 25V",
                "pkg": "Radial Can",
                "qty": 25,
                "location": "Cabinet C - Drawer 2 - Bin 100U",
                "state": "Reusable",  # tested pass
                "test_method": "DER EE DE-5000 LCR Meter 1kHz",
                "exp_val": 100.0,
                "meas_val": 98.4,
                "unit": "uF",
                "tol": 10.0,
            },
            {
                "code": "CMP-2026-0202",
                "device_code": "DEV-2026-0002",
                "type": "Capacitor",
                "name": "10uF 50V Tantalum Bead Capacitor",
                "part_number": "TAP106K050SCS",
                "spec": "10uF 50V 10% Solid Tantalum",
                "rated_value": "10uF 50V",
                "pkg": "Radial Bead",
                "qty": 15,
                "location": "Cabinet C - Drawer 1 - Bin 10U",
                "state": "Needs Testing",  # untested
            },
            {
                "code": "CMP-2026-0203",
                "device_code": "DEV-2026-0001",
                "type": "Capacitor",
                "name": "1000uF 16V Filter Capacitor (Defective/Bulged)",
                "part_number": "CAP-1000U-16V",
                "spec": "1000uF 16V High ESR Leaking Electrolytic",
                "rated_value": "1000uF 16V",
                "pkg": "Radial Can",
                "qty": 8,
                "location": "Quarantine Reject Bin",
                "state": "Rejected",  # tested fail
                "test_method": "ESR & Leakage Current Meter",
                "exp_val": 1000.0,
                "meas_val": 420.0,
                "unit": "uF",
                "tol": 20.0,
            },
            # Diodes & LEDs
            {
                "code": "CMP-2026-0301",
                "device_code": "DEV-2026-0002",
                "type": "Diode",
                "name": "1N4007 1A 1000V Silicon Rectifier Diode",
                "part_number": "1N4007",
                "spec": "1A 1000V Standard Recovery Power Diode",
                "rated_value": "1A 1000V",
                "pkg": "DO-41 Axial",
                "qty": 35,
                "location": "Cabinet D - Drawer 1 - Bin 4007",
                "state": "Reusable",  # tested pass
                "test_method": "Diode Vf Check @ 10mA",
                "exp_val": 0.7,
                "meas_val": 0.68,
                "unit": "V",
                "tol": 10.0,
            },
            {
                "code": "CMP-2026-0302",
                "device_code": "DEV-2026-0004",
                "type": "Diode",
                "name": "5mm High-Efficiency Green Indicator LED",
                "part_number": "LED-5MM-GRN",
                "spec": "2.2V 20mA 565nm Diffused Green LED",
                "rated_value": "2.2V 20mA",
                "pkg": "Through-Hole 5mm Round",
                "qty": 45,
                "location": "Cabinet D - Drawer 2 - Bin LED",
                "state": "Reusable",  # tested pass
                "test_method": "Bench PSU Constant Current 20mA",
                "exp_val": 2.2,
                "meas_val": 2.15,
                "unit": "V",
                "tol": 5.0,
            },
            # Transistors
            {
                "code": "CMP-2026-0401",
                "device_code": "DEV-2026-0003",
                "type": "Transistor",
                "name": "2N2222A NPN General Purpose Switching BJT",
                "part_number": "2N2222A",
                "spec": "40V 800mA 300MHz NPN Transistor",
                "rated_value": "40V 800mA",
                "pkg": "TO-92",
                "qty": 20,
                "location": "Cabinet T - Drawer 1 - Bin 2222",
                "state": "Reusable",  # tested pass
                "test_method": "Transistor Tester hFE Verification",
                "exp_val": 150.0,
                "meas_val": 185.0,
                "unit": "hFE",
                "tol": 30.0,
            },
            {
                "code": "CMP-2026-0402",
                "device_code": "DEV-2026-0003",
                "type": "Transistor",
                "name": "BC547 Low Noise Audio NPN BJT",
                "part_number": "BC547B",
                "spec": "45V 100mA Low Noise NPN Small Signal",
                "rated_value": "45V 100mA",
                "pkg": "TO-92",
                "qty": 25,
                "location": "Cabinet T - Drawer 1 - Bin 547",
                "state": "Needs Testing",  # untested
            },
            {
                "code": "CMP-2026-0403",
                "device_code": "DEV-2026-0002",
                "type": "Transistor",
                "name": "IRF540N N-Channel Power MOSFET (Short-Circuit Defective)",
                "part_number": "IRF540N",
                "spec": "100V 33A 44mOhm Power MOSFET",
                "rated_value": "100V 33A",
                "pkg": "TO-220AB",
                "qty": 5,
                "location": "Quarantine Reject Bin",
                "state": "Rejected",  # tested fail (gate shorted)
                "test_method": "Curve Tracer Vgs/Rds(on) Check",
                "exp_val": 4.0,
                "meas_val": 0.05,
                "unit": "V",
                "tol": 10.0,
            },
            # Integrated Circuits
            {
                "code": "CMP-2026-0501",
                "device_code": "DEV-2026-0003",
                "type": "Integrated Circuit",
                "name": "NE555P Precision Monostable/Astable Timer IC",
                "part_number": "NE555P",
                "spec": "Standard Bipolar 555 Timer DIP-8",
                "rated_value": "4.5V - 16V",
                "pkg": "DIP-8",
                "qty": 18,
                "location": "Cabinet IC - Drawer 1 - Bin 555",
                "state": "Reusable",  # tested pass
                "test_method": "Astable 1kHz Oscillation & Duty Cycle Breadboard Test",
                "exp_val": 1000.0,
                "meas_val": 995.0,
                "unit": "Hz",
                "tol": 5.0,
            },
            {
                "code": "CMP-2026-0502",
                "device_code": "DEV-2026-0001",
                "type": "Integrated Circuit",
                "name": "LM7805 5V 1.5A Positive Linear Voltage Regulator",
                "part_number": "LM7805CT",
                "spec": "5V Fixed Output 1.5A Linear Regulator",
                "rated_value": "5.0V Output",
                "pkg": "TO-220",
                "qty": 15,
                "location": "Cabinet IC - Drawer 2 - Bin 7805",
                "state": "Reusable",  # tested pass
                "test_method": "Bench Load Regulation 12V in -> 1A load",
                "exp_val": 5.0,
                "meas_val": 4.98,
                "unit": "V",
                "tol": 2.0,
            },
            {
                "code": "CMP-2026-0503",
                "device_code": "DEV-2026-0003",
                "type": "Integrated Circuit",
                "name": "LM741 Operational Amplifier IC",
                "part_number": "LM741CN",
                "spec": "Classic General Purpose Single Op-Amp",
                "rated_value": "+/-15V",
                "pkg": "DIP-8",
                "qty": 12,
                "location": "Cabinet IC - Drawer 1 - Bin 741",
                "state": "Needs Testing",  # untested
            },
            # Relays & Switches
            {
                "code": "CMP-2026-0601",
                "device_code": "DEV-2026-0004",
                "type": "Relay",
                "name": "5V SPDT Miniature Power PCB Relay",
                "part_number": "SRD-05VDC-SL-C",
                "spec": "5V Coil 10A 250VAC Switching Relay",
                "rated_value": "5VDC 10A",
                "pkg": "Sealed PCB",
                "qty": 10,
                "location": "Cabinet SW - Drawer 1 - Bin RLY",
                "state": "Reusable",  # tested pass
                "test_method": "5V Coil Actuation & Contact Resistance Milliohm Test",
                "exp_val": 70.0,
                "meas_val": 71.2,
                "unit": "Ohm",
                "tol": 10.0,
            },
            # Connectors
            {
                "code": "CMP-2026-0701",
                "device_code": "DEV-2026-0001",
                "type": "Connector",
                "name": "40-Pin 2.54mm Breakaway Male Pin Header Strip",
                "part_number": "HDR-40P-2.54",
                "spec": "1x40 Straight Gold-Plated Pin Header 0.1 inch",
                "rated_value": "3A 250V",
                "pkg": "Through-Hole 2.54mm",
                "qty": 30,
                "location": "Cabinet CN - Drawer 1 - Bin HDR",
                "state": "Reusable",  # tested pass
                "test_method": "Visual Alignment & Continuity Matrix Check",
                "exp_val": 0.0,
                "meas_val": 0.02,
                "unit": "Ohm",
                "tol": 1.0,
            },
        ]

        components_map = {}
        for cdata in components_to_seed:
            comp = Component.query.filter_by(component_code=cdata["code"]).first()
            ctype = types_map.get(cdata["type"], types_map["Other"])
            dev = devices_map.get(cdata["device_code"])

            if not comp:
                # Generate QR image
                qr_file = generate_component_qr(cdata["code"], base_url="")

                # Initial status: untested by rule, then updated by test if Reusable/Rejected
                health_status = "untested"
                health_score = None

                comp = Component(
                    component_code=cdata["code"],
                    device_id=dev.id if dev else None,
                    type_id=ctype.id,
                    name=cdata["name"],
                    part_number=cdata.get("part_number"),
                    specification=cdata.get("spec"),
                    rated_value=cdata.get("rated_value"),
                    package_type=cdata.get("pkg"),
                    quantity_total=cdata["qty"],
                    quantity_available=cdata["qty"],
                    storage_location=cdata.get("location"),
                    health_status=health_status,
                    health_score=health_score,
                    recovered_by=admin_user.id,
                    recovered_at=date.today() - timedelta(days=12),
                    qr_filename=qr_file,
                    created_at=datetime.utcnow() - timedelta(days=12),
                )
                db.session.add(comp)
                db.session.flush()

                # Record initial stock ledger entry
                initial_txn = StockTransaction(
                    component_id=comp.id,
                    request_id=None,
                    txn_type="recovery",
                    quantity_change=comp.quantity_total,
                    balance_after=comp.quantity_available,
                    performed_by=admin_user.id,
                    remarks=f"Initial recovery of {comp.quantity_total} units",
                    created_at=datetime.utcnow() - timedelta(days=12),
                )
                db.session.add(initial_txn)

                # If Reusable or Rejected, simulate recorded electrical test to transition state
                if cdata["state"] == "Reusable":
                    test = ComponentTest(
                        component_id=comp.id,
                        tested_by=admin_user.id,
                        test_method=cdata.get("test_method", "Electrical Parameter Verification"),
                        expected_value=cdata.get("exp_val"),
                        measured_value=cdata.get("meas_val"),
                        unit=cdata.get("unit"),
                        tolerance_pct=cdata.get("tol"),
                        visual_ok=True,
                        result="pass",
                        health_score=95,
                        notes="Passed laboratory electrical test. Within acceptable tolerance.",
                        tested_at=datetime.utcnow() - timedelta(days=10),
                    )
                    db.session.add(test)
                    comp.health_status = "good"
                    comp.health_score = 95

                elif cdata["state"] == "Rejected":
                    test = ComponentTest(
                        component_id=comp.id,
                        tested_by=admin_user.id,
                        test_method=cdata.get("test_method", "Parameter Fault Test"),
                        expected_value=cdata.get("exp_val"),
                        measured_value=cdata.get("meas_val"),
                        unit=cdata.get("unit"),
                        tolerance_pct=cdata.get("tol"),
                        visual_ok=False,
                        result="fail",
                        health_score=15,
                        notes="Failed electrical test; out of tolerance / internal breakdown.",
                        tested_at=datetime.utcnow() - timedelta(days=10),
                    )
                    db.session.add(test)
                    comp.health_status = "faulty"
                    comp.health_score = 15

                print(f"Created component: {comp.component_code} ({comp.name}) -> Status: {comp.display_status}")
            components_map[cdata["code"]] = comp
        db.session.commit()

        # 5. Component Requests and Reuse Transactions
        requests_to_seed = [
            # Completed & Approved Request 1
            {
                "comp_code": "CMP-2026-0101",  # 10k resistor
                "requester": student_user,
                "qty": 5,
                "project": "Mini Project: Automatic Night Light Circuit",
                "purpose": "Voltage divider circuit using LDR and transistor switch.",
                "status": "approved",
                "admin_remarks": "Approved. Components issued for ECE Lab Table 4.",
            },
            # Completed & Approved Request 2
            {
                "comp_code": "CMP-2026-0501",  # 555 Timer IC
                "requester": student_rohan,
                "qty": 2,
                "project": "ECE Lab: PWM DC Motor Speed Controller",
                "purpose": "Astable 555 pulse generator for MOSFET gate driving.",
                "status": "approved",
                "admin_remarks": "Approved. Tested timer ICs issued from Bin 555.",
            },
            # Pending Request
            {
                "comp_code": "CMP-2026-0502",  # 7805 regulator
                "requester": student_user,
                "qty": 1,
                "project": "Capstone: IoT Environmental Sensor Node",
                "purpose": "Regulating 9V battery input down to 5.0V for MCU.",
                "status": "pending",
                "admin_remarks": None,
            },
            # Rejected Request
            {
                "comp_code": "CMP-2026-0201",  # 100uF capacitor
                "requester": student_rohan,
                "qty": 20,
                "project": "Class Demo Amplifier",
                "purpose": "High bulk power decoupling.",
                "status": "rejected",
                "admin_remarks": "Rejected: Requested batch exceeds single student allocation limits.",
            },
        ]

        for rdata in requests_to_seed:
            comp = components_map.get(rdata["comp_code"])
            if not comp:
                continue

            existing_req = ComponentRequest.query.filter_by(
                component_id=comp.id,
                requester_id=rdata["requester"].id,
                project_name=rdata["project"],
            ).first()

            if not existing_req:
                req = ComponentRequest(
                    component_id=comp.id,
                    requester_id=rdata["requester"].id,
                    quantity=rdata["qty"],
                    project_name=rdata["project"],
                    purpose=rdata["purpose"],
                    status=rdata["status"],
                    reviewed_by=admin_user.id if rdata["status"] != "pending" else None,
                    reviewed_at=datetime.utcnow() - timedelta(days=2) if rdata["status"] != "pending" else None,
                    admin_remarks=rdata["admin_remarks"],
                    created_at=datetime.utcnow() - timedelta(days=5),
                )
                db.session.add(req)
                db.session.flush()

                # If approved, deduct stock and record reuse transaction!
                if rdata["status"] == "approved":
                    if comp.quantity_available >= rdata["qty"]:
                        comp.quantity_available -= rdata["qty"]

                        reuse_txn = StockTransaction(
                            component_id=comp.id,
                            request_id=req.id,
                            txn_type="issue",
                            quantity_change=-rdata["qty"],
                            balance_after=comp.quantity_available,
                            performed_by=admin_user.id,
                            remarks=f"Issued for project '{req.project_name}'",
                            created_at=datetime.utcnow() - timedelta(days=2),
                        )
                        db.session.add(reuse_txn)

                print(f"Created request #{req.id} for {comp.name} -> {req.status}")
        db.session.commit()

        # 6. Initial Audit Log Entry
        if not AuditLog.query.first():
            log = AuditLog(
                user_id=admin_user.id,
                action="SYSTEM_INITIALIZED",
                entity="System",
                entity_id=1,
                details="Seeded initial demo devices, components across 8 categories, and test records.",
                created_at=datetime.utcnow(),
            )
            db.session.add(log)
            db.session.commit()

        print("\n=== Database Seeding Completed Successfully! ===")
        print("Demo Credentials:")
        print("  Administrator: admin@ewaste.edu / Admin@123")
        print("  Student:       student@ewaste.edu / Student@123")
        print("  Student 2:     rohan.ece@ewaste.edu / Student@123")


if __name__ == "__main__":
    seed_database()
