from Galaxy import Galaxy
from StarGalaxy import StarGalaxy
from Orbit import Orbit
import numpy as np
import tqdm


class Sim:

    def MakeGalaxy(self):
        # Constants
        galmass = 4.8
        ahalo = 0.1
        vhalo = 1.0
        rthalo = 5.0
        galpos = np.full((3, 1), 0.)
        galvel = np.full((3, 1), 0.)
        diskSize = 2.5

        # Initial conditions
        galtheta = float(input("galtheta(은하 1의 세타) > "))
        galphi = float(input("galphi(은하 1의 파이) > "))
        comptheta = float(input("comptheta(은하 2의 세타) > "))
        compphi = float(input("compphi(은하 2의 파이) > "))
        total_star_num = int(input("total_star_num(전체 별의 수) > "))
        galn = int(0.5*total_star_num)
        compn = int(0.5*total_star_num)

        self.galaxy = StarGalaxy(galmass, ahalo, vhalo, rthalo, galpos, galvel, diskSize, galtheta, galphi, galn)
        self.companion = StarGalaxy(galmass, ahalo, vhalo, rthalo, galpos, galvel, diskSize, comptheta, compphi, compn)

    def MakeOrbit(self):
        energy = 0
        eccentricity = 1
        rperi = 3.0

        tperi = float(input("두 은하 사이 거리> "))
        massratio = float(input("은하 1에 대한 은하 2의 질량비 > "))
        self.companion.scaleMass(massratio)

        self.crashOrbit = Orbit(energy, rperi, tperi, eccentricity, self.galaxy.galmass, self.companion.galmass, self.galaxy.galpos, self.companion.galpos, self.galaxy.galvel, self.companion.galvel)

        self.galaxy.setPosvel(self.crashOrbit.bod1pos, self.crashOrbit.bod1vel)
        self.companion.setPosvel(self.crashOrbit.bod2pos, self.crashOrbit.bod2vel)

    def RunSim(self):
        frames = []
        dt = 0.04
        max_frame = int(input("최대 프레임 수 > "))
        tmax = max_frame * dt
        self.galaxy.InitStars()
        self.companion.InitStars()
        frames.append([self.galaxy.starpos, self.companion.starpos])
        for t in tqdm.tqdm(np.arange(0, tmax, dt), desc="진행도"):
            dist = 3.5 * np.linalg.norm((self.galaxy.galpos - self.companion.galpos))
            self.galaxy.galacc = self.companion.Acceleration(self.galaxy.galpos)
            self.companion.galacc = self.galaxy.Acceleration(self.companion.galpos)

            self.galaxy.galacc = self.galaxy.galacc + self.companion.DynFric(self.galaxy.InteriorMass(dist/3.5), self.galaxy.galpos, self.galaxy.galvel)
            self.companion.galacc = self.companion.galacc + self.galaxy.DynFric(self.companion.InteriorMass(dist/3.5), self.companion.galpos, self.companion.galvel)

            comacc = ((self.galaxy.galmass * self.galaxy.galacc) + (self.companion.galmass * self.companion.galacc))/(self.galaxy.galmass + self.companion.galmass)
            self.galaxy.galacc = self.galaxy.galacc - comacc
            self.companion.galacc = self.companion.galacc - comacc

            self.galaxy.staracc = self.galaxy.Acceleration(self.galaxy.starpos) + self.companion.Acceleration(self.galaxy.starpos)
            self.companion.staracc = self.galaxy.Acceleration(self.companion.starpos) + self.companion.Acceleration(self.companion.starpos)

            self.galaxy.MoveStars(dt)
            self.companion.MoveStars(dt)
            self.galaxy.MoveGalaxy(dt)
            self.companion.MoveGalaxy(dt)
            frames.append([self.galaxy.starpos, self.companion.starpos])
        return frames

if __name__ == '__main__':
    sim = Sim()
    sim.MakeGalaxy()
    sim.MakeOrbit()
    frames = sim.RunSim()
    frames = np.array(frames[:-1])
    np.save('simulation.npy', frames)