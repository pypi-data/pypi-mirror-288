import math
import numpy as np

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
        return 2 ** (10 * (t - 1))

    def out(self, t):
        return 1 - 2 ** (-10 * t)

    def in_out(self, t):
        return 0.5 * (2 ** (10 * (t - 1)) if t < 0.5 else 2 - 2 ** (-10 * t))

    def out_in(self, t):
        return 0.5 * (2 ** (10 * (t - 1)) if t < 0.5 else 2 - 2 ** (-10 * (t - 0.5)))

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
        return 0.5 * self.out(t * 2) if t < 0.5 else 0.5 * self.in_(t * 2 - 1) + 0.5

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
        return 0.5 * self.out(t * 2) if t < 0.5 else 0.5 * self.in_(t * 2 - 1) + 0.5

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    def get_easing_class(easing_type):
        easing_classes = {
            'Exponential': Exponential,
            'Quad': Quad,
            'Back': Back,
            'Bounce': Bounce,
            'Elastic': Elastic,
        }
        return easing_classes.get(easing_type, lambda: EasingFunction())

    def plot_easing(easing_type):
        easing_class = get_easing_class(easing_type)()
        t_values = np.linspace(0, 1, 500)
        in_values = [easing_class.in_(t) for t in t_values]
        out_values = [easing_class.out(t) for t in t_values]
        in_out_values = [easing_class.in_out(t) for t in t_values]
        out_in_values = [easing_class.out_in(t) for t in t_values]
        
        plt.figure(figsize=(10, 8))
        plt.plot(t_values, in_values, label='In')
        plt.plot(t_values, out_values, label='Out')
        plt.plot(t_values, in_out_values, label='InOut')
        plt.plot(t_values, out_in_values, label='OutIn')
        plt.title(f'Easing Functions: {easing_type}')
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.legend()
        plt.grid(True)
        plt.show()

    easing_types = ['Exponential', 'Quad', 'Back', 'Bounce', 'Elastic']
    for easing_type in easing_types:
        plot_easing(easing_type)