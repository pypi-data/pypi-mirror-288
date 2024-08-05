# SPDX-FileCopyrightText: 2024-present U.N. Owen <void@some.where>
#
# SPDX-License-Identifier: MIT

import requests
import __about__


def main():
    print('hello rpa-test-zhang')
    print('requests:' + requests.__version__)
    print('rpa_test_zhang:' + __about__.__version__)



if __name__ == '__main__':
    main()