#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: QPSK_CFO
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import blocks
import math
import numpy
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip



class QPSK_CFO(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "QPSK_CFO", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("QPSK_CFO")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "QPSK_CFO")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.sym_map = sym_map = [1+1j,1-1j,-1+1j,-1-1j]
        self.sps = sps = 4
        self.samp_rate = samp_rate = 1e6
        self.qpsk = qpsk = digital.constellation_rect(sym_map, [0, 1, 2, 3],
        4, 2, 2, 1, 1).base()
        self.frequency_shift = frequency_shift = -1e4
        self.excess_bw = excess_bw = 0.75

        ##################################################
        # Blocks
        ##################################################

        self._frequency_shift_range = qtgui.Range(-1e6, 1e6, 1e4, -1e4, 200)
        self._frequency_shift_win = qtgui.RangeWidget(self._frequency_shift_range, self.set_frequency_shift, "'frequency_shift'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._frequency_shift_win)
        self.root_raised_cosine_filter_0_0 = filter.fir_filter_ccf(
            1,
            firdes.root_raised_cosine(
                1,
                samp_rate,
                (samp_rate/sps),
                excess_bw,
                128))
        self.root_raised_cosine_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.root_raised_cosine(
                1,
                samp_rate,
                (samp_rate/sps),
                excess_bw,
                128))
        self.qtgui_sink_x_0_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_0_win)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccc(4, [1,0,0,0])
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.fir_filter_xxx_1_0 = filter.fir_filter_ccc(4, [1,0,0,0])
        self.fir_filter_xxx_1_0.declare_sample_delay(0)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_ic(sym_map, 1)
        self.blocks_throttle2_0_0 = blocks.throttle( gr.sizeof_gr_complex*1, (samp_rate/4), True, 0 if "auto" == "auto" else max( int(float(0.1) * (samp_rate/4)) if "auto" == "time" else int(0.1), 1) )
        self.blocks_freqshift_cc_0_0 = blocks.rotator_cc(2.0*math.pi*frequency_shift/samp_rate)
        self.blocks_freqshift_cc_0 = blocks.rotator_cc(2.0*math.pi*1e4/samp_rate)
        self.blocks_float_to_int_0 = blocks.float_to_int(1, 1)
        self.blocks_char_to_float_2 = blocks.char_to_float(1, 1)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 4, 100000))), True)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_char_to_float_2, 0))
        self.connect((self.blocks_char_to_float_2, 0), (self.blocks_float_to_int_0, 0))
        self.connect((self.blocks_float_to_int_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_freqshift_cc_0, 0), (self.blocks_freqshift_cc_0_0, 0))
        self.connect((self.blocks_freqshift_cc_0_0, 0), (self.root_raised_cosine_filter_0_0, 0))
        self.connect((self.blocks_throttle2_0_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_throttle2_0_0, 0))
        self.connect((self.fir_filter_xxx_1_0, 0), (self.qtgui_sink_x_0_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.root_raised_cosine_filter_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.blocks_freqshift_cc_0, 0))
        self.connect((self.root_raised_cosine_filter_0_0, 0), (self.fir_filter_xxx_1_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "QPSK_CFO")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_sym_map(self):
        return self.sym_map

    def set_sym_map(self, sym_map):
        self.sym_map = sym_map
        self.digital_chunks_to_symbols_xx_0.set_symbol_table(self.sym_map)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, (self.samp_rate/self.sps), self.excess_bw, 128))
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, (self.samp_rate/self.sps), self.excess_bw, 128))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*1e4/self.samp_rate)
        self.blocks_freqshift_cc_0_0.set_phase_inc(2.0*math.pi*self.frequency_shift/self.samp_rate)
        self.blocks_throttle2_0_0.set_sample_rate((self.samp_rate/4))
        self.qtgui_sink_x_0_0.set_frequency_range(0, self.samp_rate)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, (self.samp_rate/self.sps), self.excess_bw, 128))
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, (self.samp_rate/self.sps), self.excess_bw, 128))

    def get_qpsk(self):
        return self.qpsk

    def set_qpsk(self, qpsk):
        self.qpsk = qpsk

    def get_frequency_shift(self):
        return self.frequency_shift

    def set_frequency_shift(self, frequency_shift):
        self.frequency_shift = frequency_shift
        self.blocks_freqshift_cc_0_0.set_phase_inc(2.0*math.pi*self.frequency_shift/self.samp_rate)

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, (self.samp_rate/self.sps), self.excess_bw, 128))
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, (self.samp_rate/self.sps), self.excess_bw, 128))




def main(top_block_cls=QPSK_CFO, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
