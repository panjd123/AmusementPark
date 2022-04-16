#include <bits/stdc++.h>
using namespace std;
const int BitLen = 6e4;
class BigNum;
BigNum _add(const BigNum& a, const BigNum& b);
BigNum _minus(const BigNum& a, const BigNum& b);
BigNum _mul(const BigNum& a, const BigNum& b);
BigNum _div(const BigNum& a, const BigNum& b);
class BigNum {
   public:
    int s[BitLen], sg, len;
    BigNum(int rhs = 0) {
        sg = 1;
        memset(s, 0, sizeof s);
        if (!rhs) {
            len = 1;
            sg = 1;
        } else {
            if (rhs < 0) {
                sg = -1;
                rhs = -rhs;
            } else
                sg = 1;
            for (len = 0; rhs; len++, rhs /= 10)
                s[len] = rhs % 10;
        }
    }
    BigNum(long long rhs) {
        sg = 1;
        memset(s, 0, sizeof s);
        if (rhs == 0) {
            len = 1;
            sg = 1;
        } else {
            if (rhs < 0) {
                sg = -1;
                rhs = -rhs;
            } else
                sg = 1;
            for (len = 0; rhs; len++, rhs /= 10)
                s[len] = rhs % 10;
        }
    }
    BigNum(const char str[]) {
        sg = 1;
        if (*str == '-') {
            sg = -1;
            str++;
        } else if (*str == '+') {
            sg = 1;
            str++;
        }
        len = strlen(str);
        for (int i = len - 1; i >= 0; i--) {
            s[i] = *str - '0';
            str++;
        }
    }
    friend istream& operator>>(istream& in, BigNum& x);
    friend ostream& operator<<(istream& out, BigNum& x);
    friend ostream& operator<<(istream& out, BigNum&& x);
    int operator[](int i) const { return s[i]; }
    int& operator[](int i) { return s[i]; }
    long long to_ll() const {
        long long res = 0;
        for (int i = 0, f = 1; i < len; i++, f *= 10)
            res += s[i] * f;
        return sg * res;
    }
    BigNum operator=(const long long& rhs) {
        long long t = abs(rhs);
        if (rhs < 0)
            sg = -1;
        else
            sg = 1;
        for (len = 0; t; len++, t /= 10)
            s[len] = t % 10;
        return *this;
    }
    BigNum operator=(const int& rhs) {
        *this = (long long)rhs;
        return *this;
    }
    BigNum operator=(const char str[]) {
        if (*str == '-') {
            sg = -1;
            str++;
        } else if (*str == '+') {
            sg = 1;
            str++;
        }
        len = strlen(str);
        for (int i = len - 1; i >= 0; i--) {
            s[i] = *str - '0';
            str++;
        }
        return *this;
    }
    bool operator<(const BigNum& rhs) const {
        if (sg != rhs.sg)
            return sg < rhs.sg;
        if (len != rhs.len)
            return (len < rhs.len) ^ (sg == -1);
        for (int i = len - 1; i >= 0; i--)
            if (s[i] != rhs.s[i])
                return (s[i] < rhs.s[i]) ^ (sg == -1);
        return 0;
    }
    bool operator>(const BigNum& rhs) const {
        if (sg != rhs.sg)
            return sg > rhs.sg;
        if (len != rhs.len)
            return (len > rhs.len) ^ (sg == -1);
        for (int i = len - 1; i >= 0; i--)
            if (s[i] != rhs.s[i])
                return (s[i] > rhs.s[i]) ^ (sg == -1);
        return 0;
    }
    bool operator==(const BigNum& rhs) const {
        if (s[len - 1] == 0 && rhs[rhs.len - 1] == 0)
            return 1;
        if (sg != rhs.sg)
            return 0;
        if (len != rhs.len)
            return 0;
        for (int i = len - 1; i >= 0; i--)
            if (s[i] != rhs.s[i])
                return 0;
        return 1;
    }
    // bool operator==(const int rhs) const { return *this == BigNum(rhs); }
    bool operator!=(const int rhs) const { return !(*this == BigNum(rhs)); }
    bool operator<(const int rhs) const {  // for +-
        if (!rhs)
            return sg < 0;
        return *this < BigNum(rhs);
    }
    bool operator>(const int rhs) const {  // for +-
        if (!rhs)
            return sg > 0;
        return *this > BigNum(rhs);
    }
    bool operator>=(const int& rhs) const {
        return *this > rhs || *this == rhs;
    }
    bool operator<=(const int& rhs) const {
        return *this < rhs || *this == rhs;
    }
    bool operator>=(const BigNum& rhs) const {
        return *this > rhs || *this == rhs;
    }
    bool operator<=(const BigNum& rhs) const {
        return *this < rhs || *this == rhs;
    }
    BigNum operator-() const {
        BigNum res;
        res = *this;
        res.sg = -res.sg;
        return res;
    }
    BigNum operator+(const BigNum& rhs) const {
        if (*this > 0 && rhs > 0)
            return _add(*this, rhs);
        if (*this < 0 && rhs < 0)
            return -_add(*this, rhs);
        if (*this > 0 && rhs < 0)
            return _minus(*this, rhs);
        if (*this < 0 && rhs > 0)
            return _minus(rhs, *this);
        if (*this == 0)
            return rhs;
        else
            return *this;
    }
    BigNum operator+(const long long& rhs) const { return *this + BigNum(rhs); }
    BigNum operator+=(const BigNum& rhs) { return *this = *this + BigNum(rhs); }
    BigNum operator+=(const long long& rhs) { return *this = *this + BigNum(rhs); }
    BigNum operator-(const BigNum& rhs) const {
        if (*this > 0 && rhs > 0)
            return _minus((*this).getabs(), rhs.getabs());
        if (*this < 0 && rhs < 0)
            return _minus(rhs.getabs(), (*this).getabs());
        if (*this > 0 && rhs < 0)
            return _add((*this).getabs(), rhs.getabs());
        if (*this < 0 && rhs > 0)
            return -_add((*this).getabs(), rhs.getabs());
        if (*this == 0)
            return -rhs;
        else
            return *this;
    }
    BigNum operator-(const int& rhs) const { return *this - BigNum(rhs); }
    BigNum operator-=(const BigNum& rhs) { return *this = *this - BigNum(rhs); }
    BigNum operator-=(const int& rhs) { return *this = *this - BigNum(rhs); }
    BigNum operator*(const BigNum& rhs) const {
        BigNum res = _mul(*this, rhs);
        res.sg = sg * rhs.sg;
        return res;
    }
    BigNum operator*(const int& rhs) const { return *this * BigNum(rhs); }
    BigNum operator*=(const BigNum& rhs) { return *this = *this * BigNum(rhs); }
    BigNum operator*(const int& rhs) { return *this = *this * BigNum(rhs); }
    BigNum operator/(const BigNum& rhs) const {
        BigNum res = _div((*this).getabs(), rhs.getabs());
        res.sg = sg * rhs.sg;
        return res;
    }
    BigNum operator/(const int& rhs) const { return *this / BigNum(rhs); }
    BigNum operator/=(const BigNum& rhs) { return *this = *this / rhs; }
    BigNum operator/=(const int& rhs) { return *this = *this / BigNum(rhs); }
    BigNum operator%(const BigNum& rhs) const {
        return *this - *this / rhs * rhs;
    }
    BigNum operator%(const int& rhs) const {
        return *this - *this / BigNum(rhs) * BigNum(rhs);
    }
    BigNum operator%=(const BigNum& rhs) { return *this = *this % rhs; }
    BigNum operator%=(const int& rhs) { return *this = *this % BigNum(rhs); }
    BigNum sub(const int l, const int r) const {
        // begin with 1
        BigNum res;
        res.len = 0;
        for (int i = len - r; i <= len - l; i++)
            res[res.len++] = s[i];
        return res;
    }
    BigNum getabs() const {
        BigNum res = *this;
        res.sg = 1;
        return res;
    }
    void out() {
        cout << sg << " " << len << endl;
        for (int i = 0; i < len; i++)
            cout << s[i] << " ";
        cout << endl
             << "-----" << endl;
    }
    void out() const {
        cout << sg << " " << len << endl;
        for (int i = 0; i < len; i++)
            cout << s[i] << " ";
        cout << endl
             << "-----" << endl;
    }
};
istream& operator>>(istream& in, BigNum& a) {
    char s[BitLen];
    in >> s;
    if (s[0] == '-') {
        a.sg = -1;
        a.len = strlen(s) - 1;
        for (int i = 0; i < a.len; i++)
            a.s[i] = s[a.len - i] - '0';
    } else {
        a.sg = 1;
        a.len = strlen(s);
        for (int i = 0; i < a.len; i++)
            a.s[i] = s[a.len - i - 1] - '0';
    }
    return in;
}
ostream& operator<<(ostream& out, BigNum& a) {
    if (a.sg == -1 && a != 0)
        out << "-";
    for (int i = a.len - 1; i >= 0; i--)
        out << a.s[i];
    return out;
}
ostream& operator<<(ostream& out, BigNum&& a) {
    if (a.sg == -1 && a != 0)
        out << "-";
    for (int i = a.len - 1; i >= 0; i--)
        out << a.s[i];
    return out;
}
BigNum _add(const BigNum& a, const BigNum& b) {
    BigNum res;
    int lm = max(a.len, b.len);
    for (int i = 0; i < lm; i++) {
        res[i] += a[i] + b[i];
        res[i + 1] += res[i] / 10;
        res[i] %= 10;
    }
    if (res[lm])
        lm++;
    res.len = lm;
    return res;
}
BigNum _minus(const BigNum& a, const BigNum& b) {
    if (a.getabs() < b.getabs())
        return -_minus(b, a);
    BigNum res;
    int lm = max(a.len, b.len);
    for (int i = 0; i < lm; i++) {
        res[i] += a[i] - b[i];
        if (res[i] < 0) {
            res[i] += 10;
            res[i + 1]--;
        }
    }
    while (res[lm - 1] == 0 && lm > 1)
        lm--;
    res.len = lm;
    return res;
}
BigNum _mul(const BigNum& a, const BigNum& b) {
    BigNum res;
    if (a == 0 || b == 0)
        return res;
    for (int i = 0; i < a.len; i++) {
        for (int j = 0; j < b.len; j++) {
            res[i + j] += a[i] * b[j];
            res[i + j + 1] += res[i + j] / 10;
            res[i + j] %= 10;
        }
    }
    if (res[a.len + b.len - 1])
        res.len = a.len + b.len;
    else
        res.len = a.len + b.len - 1;
    return res;
}
BigNum _div(const BigNum& a, const BigNum& b) {
    BigNum res, t = a.sub(1, b.len);
    if (a < b)
        return res;
    int ans[BitLen];
    for (int i = 0; i <= a.len - b.len; i++) {
        for (int j = 9; j >= 0; j--) {
            if (t.getabs() >= (b * j).getabs()) {
                t -= b * j;
                ans[i] = j;
                break;
            }
        }
        t = t * 10 + ((a.len - i - 1 - b.len >= 0) ? a[a.len - i - 1 - b.len] : 0);
    }
    res.len = 0;
    if (ans[0] == 0) {
        for (int i = a.len - b.len; i >= 1; i--) {
            res[res.len++] = ans[i];
        }
    } else {
        for (int i = a.len - b.len; i >= 0; i--) {
            res[res.len++] = ans[i];
        }
    }
    return res;
}
BigNum Pow(BigNum x, int p) {
    BigNum ret = 1;
    while (p) {
        if (p & 1)
            ret *= x;
        x *= x;
        p >>= 1;
    }
    return ret;
}
BigNum x = 999999, y = 1;
int main() {
    cout << Pow(x, 999) << endl;
}