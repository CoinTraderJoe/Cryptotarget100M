// Copyright (c) 2011-2014 The Cryptotarget100M developers
// Distributed under the MIT/X11 software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#ifndef CRYPTOTARGET100MADDRESSVALIDATOR_H
#define CRYPTOTARGET100MADDRESSVALIDATOR_H

#include <QValidator>

/** Base58 entry widget validator, checks for valid characters and
 * removes some whitespace.
 */
class Cryptotarget100MAddressEntryValidator : public QValidator
{
    Q_OBJECT

public:
    explicit Cryptotarget100MAddressEntryValidator(QObject *parent);

    State validate(QString &input, int &pos) const;
};

/** Cryptotarget100M address widget validator, checks for a valid cryptotarget100M address.
 */
class Cryptotarget100MAddressCheckValidator : public QValidator
{
    Q_OBJECT

public:
    explicit Cryptotarget100MAddressCheckValidator(QObject *parent);

    State validate(QString &input, int &pos) const;
};

#endif // CRYPTOTARGET100MADDRESSVALIDATOR_H
