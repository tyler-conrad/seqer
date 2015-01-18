#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Scenic
# Copyright (C) 2008 Société des arts technologiques (SAT)
# http://www.sat.qc.ca
# All rights reserved.
#
# This file is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Scenic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Scenic. If not, see <http://www.gnu.org/licenses/>.
"""
Main runner of the app is the run() function.
"""

from rtpmidi.engines.midi.midi_session import MidiSession
from rtpmidi.protocols.rtp.rtp_control import RTPControl


def run(
        peer_address,
        sending_port,
        receiving_port,
        latency=20,
        jitter_buffer_size=10,
        safe_keyboard=False,
        disable_recovery_journal=False,
        follow_standard=False,
        verbose=False):
    midi_session_c = RTPControl().add_session(
        MidiSession(
            peer_address,
            sending_port,
            receiving_port,
            latency,
            jitter_buffer_size,
            safe_keyboard,
            disable_recovery_journal,
            follow_standard,
            verbose))
    midi_session = RTPControl().get_session(midi_session_c)
    midi_session.get_devices()
    midi_session.set_device_in(1)
    midi_session.set_device_out(0)
    RTPControl().start_session(midi_session_c)
