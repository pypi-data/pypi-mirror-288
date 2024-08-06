import math

class EasingFunction:
    def out(self, t):
        raise NotImplementedError

    def in_(self, t):
        raise NotImplementedError

    def in_out(self, t):
        raise NotImplementedError

    def out_in(self, t):
        raise NotImplementedError

class Exponential(EasingFunction):
    def in_(self, t):
        return 0 if t == 0 else 2 ** (10 * (t - 1))

    def out(self, t):
        return 1 if t == 1 else 1 - 2 ** (-10 * t)

    def in_out(self, t):
        if t == 0 or t == 1:
            return t
        t *= 2
        if t < 1:
            return 0.5 * 2 ** (10 * (t - 1))
        return 0.5 * (2 - 2 ** (-10 * (t - 1)))

    def out_in(self, t):
        if t < 0.5:
            return 0.5 * self.out(t * 2)
        return 0.5 * self.in_(t * 2 - 1) + 0.5

class Quad(EasingFunction):
    def in_(self, t):
        return t * t

    def out(self, t):
        return 1 - (1 - t) * (1 - t)

    def in_out(self, t):
        return (t / 0.5) ** 2 if t < 0.5 else 1 - ((1 - t) * (1 - t)) * 0.5

    def out_in(self, t):
        return 0.5 * (t / 0.5) ** 2 if t < 0.5 else 0.5 * (1 - ((1 - t) * (1 - t)) * 0.5)

class Back(EasingFunction):
    def in_(self, t):
        c1 = 1.70158
        c2 = c1 * 1.525
        return (t ** 2) * ((c2 + 1) * t - c2)

    def out(self, t):
        c1 = 1.70158
        c2 = c1 * 1.525
        t -= 1
        return (t ** 2) * ((c2 + 1) * t + c2) + 1

    def in_out(self, t):
        c1 = 1.70158
        c2 = c1 * 1.525
        t *= 2
        if t < 1:
            return 0.5 * (t ** 2) * ((c2 + 1) * t - c2)
        t -= 2
        return 0.5 * ((t ** 2) * ((c2 + 1) * t + c2) + 2)

    def out_in(self, t):
        if t < 0.5:
            return 0.5 * self.out(t * 2)
        return 0.5 * self.in_(t * 2 - 1) + 0.5

class Bounce(EasingFunction):
    def out(self, t):
        n1 = 7.5625
        d1 = 2.75
        if t < 1 / d1:
            return n1 * t * t
        elif t < 2 / d1:
            t -= 1.5 / d1
            return n1 * (t * t + 0.75)
        elif t < 2.5 / d1:
            t -= 2.25 / d1
            return n1 * (t * t + 0.9375)
        else:
            t -= 2.625 / d1
            return n1 * (t * t + 0.984375)

    def in_(self, t):
        return 1 - self.out(1 - t)

    def in_out(self, t):
        return 0.5 * self.in_(t * 2) if t < 0.5 else 0.5 * self.out(t * 2 - 1) + 0.5

    def out_in(self, t):
        return 0.5 * self.out(t * 2) if t < 0.5 else 0.5 * self.in_(t * 2 - 1) + 0.5

class Elastic(EasingFunction):
    def in_(self, t):
        if t == 0 or t == 1:
            return t
        p = 0.3
        s = p / 4
        return -(2 ** (10 * (t - 1))) * math.sin((t - s) * (2 * math.pi) / p)

    def out(self, t):
        if t == 0 or t == 1:
            return t
        p = 0.3
        s = p / 4
        return (2 ** (-10 * t)) * math.sin((t - s) * (2 * math.pi) / p) + 1

    def in_out(self, t):
        if t == 0 or t == 1:
            return t
        t *= 2
        p = 0.45
        s = p / 4
        if t < 1:
            return -0.5 * (2 ** (10 * (t - 1))) * math.sin((t - s) * (2 * math.pi) / p)
        return (2 ** (-10 * (t - 1))) * math.sin((t - s) * (2 * math.pi) / p) * 0.5 + 1

    def out_in(self, t):
        if t < 0.5:
            return 0.5 * self.out(t * 2)
        return 0.5 * self.in_(t * 2 - 1) + 0.5

class Sine(EasingFunction):
    def in_(self, t):
        return 1 - math.cos((t * math.pi) / 2)

    def out(self, t):
        return math.sin((t * math.pi) / 2)

    def in_out(self, t):
        return 0.5 * (1 - math.cos(math.pi * t))

    def out_in(self, t):
        if t < 0.5:
            return 0.5 * self.out(t * 2)
        return 0.5 * self.in_(t * 2 - 1) + 0.5

class Circ(EasingFunction):
    def in_(self, t):
        return 1 - math.sqrt(1 - (t ** 2))

    def out(self, t):
        t -= 1
        return math.sqrt(1 - (t ** 2))

    def in_out(self, t):
        t *= 2
        if t < 1:
            return 0.5 * (1 - math.sqrt(1 - (t ** 2)))
        t -= 2
        return 0.5 * (math.sqrt(1 - (t ** 2)) + 1)

    def out_in(self, t):
        if t < 0.5:
            return 0.5 * self.out(t * 2)
        return 0.5 * self.in_(t * 2 - 1) + 0.5

class Cubic(EasingFunction):
    def in_(self, t):
        return t ** 3

    def out(self, t):
        t -= 1
        return (t ** 3) + 1

    def in_out(self, t):
        t *= 2
        if t < 1:
            return 0.5 * (t ** 3)
        t -= 2
        return 0.5 * ((t ** 3) + 2)

    def out_in(self, t):
        if t < 0.5:
            return 0.5 * self.out(t * 2)
        return 0.5 * self.in_(t * 2 - 1) + 0.5

class Quart(EasingFunction):
    def in_(self, t):
        return t ** 4

    def out(self, t):
        t -= 1
        return (t ** 4) + 1

    def in_out(self, t):
        t *= 2
        if t < 1:
            return 0.5 * (t ** 4)
        t -= 2
        return 0.5 * ((t ** 4) + 2)

    def out_in(self, t):
        if t < 0.5:
            return 0.5 * self.out(t * 2)
        return 0.5 * self.in_(t * 2 - 1) + 0.5

class Quint(EasingFunction):
    def in_(self, t):
        return t ** 5

    def out(self, t):
        t -= 1
        return (t ** 5) + 1

    def in_out(self, t):
        t *= 2
        if t < 1:
            return 0.5 * (t ** 5)
        t -= 2
        return 0.5 * ((t ** 5) + 2)

    def out_in(self, t):
        if t < 0.5:
            return 0.5 * self.out(t * 2)
        return 0.5 * self.in_(t * 2 - 1) + 0.5

def get_easing_class(easing_type):
    easing_classes = {
        'Exponential': Exponential,
        'Quad': Quad,
        'Back': Back,
        'Bounce': Bounce,
        'Elastic': Elastic,
        'Sine': Sine,
        'Circ': Circ,
        'Cubic': Cubic,
        'Quart': Quart,
        'Quint': Quint,
    }
    return easing_classes.get(easing_type, lambda: EasingFunction())