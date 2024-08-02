class PostProcessors:
    def __init__(self, case):
        self.get = case.get

    def harmave(self, x1, x2):
        """Returns the harmonic ave of two numbers"""
        return (2 * x1 * x2) / (x1 + x2)

    def particle_balance(self):
        """Calculates the global UEDGE partcle balance"""
        from numpy import zeros, sum

        # Initialize variables
        v = {}
        for var in [
            "nxpt",
            "fnix",
            "nfsp",
            "ngsp",
            "ixrb",
            "ixlb",
            "nx",
            "ny",
            "isupgon",
            "fngx",
            "fngy",
            "fniy",
            "fniycbo",
            "ixpt1",
            "ixpt2",
        ]:
            v[var] = self.get(var)
        # Initialize balabce array if not present
        if not "balance" in dir(self):
            self.balance = {}
        # Initialize particle balance array
        self.balance["particle"] = {}
        pb = self.balance["particle"]
        for var in [
            "iirb",
            "iilb",
            "igrb",
            "iglb",
            "igpf",
            "igwall",
            "iipf",
            "iiwall",
            "iicore",
            "igcore",
            "iisep",
            "igsep",
        ]:
            pb[var] = zeros(
                (v["nxpt"], v["nfsp"] * (var[1] == "i") + v["ngsp"] * (var[1] == "g"))
            )
        # Get ranges
        pfrrange, wallrange, corerange = [], [], []
        for xpt in range(v["nxpt"]):
            corerange.append(range(v["ixpt1"][xpt] + 1, v["ixpt2"][xpt] + 1))
            pfrrange.append(
                [
                    range(v["ixlb"][xpt] + 1, v["ixpt1"][xpt] + 1),
                    range(v["ixpt2"][xpt] + 1, v["ixrb"][xpt] + 1),
                ]
            )
            wallrange.append(
                range(v["ixlb"][xpt] + 1, v["ixrb"][xpt] + 1),
            )
        # Get indices
        iycore = int(self.get("isguardc") == False)
        iysep = min(self.get("iysptrx1"), self.get("iysptrx2"))[0]
        iwall = self.get("ny")
        for xpt in range(v["nxpt"]):
            """Radial currents"""
            # Core and separatrix currents
            for ix in corerange[xpt]:
                for sp in range(v["nfsp"]):
                    pb["iicore"][xpt, sp] += (
                        v["fniy"][ix, iycore, sp] - v["fniycbo"][ix, sp]
                    ) * 1.602e-19
                    pb["iisep"][xpt, sp] += v["fniy"][ix, iysep, sp] * 1.602e-19
                for gsp in range(v["ngsp"]):
                    pb["igcore"][xpt, gsp] += v["fngy"][ix, iycore, gsp] * 1.602e-19
                    pb["iisep"][xpt, gsp] += v["fngy"][ix, iysep, gsp] * 1.602e-19
            # PFR currents
            for legrange in pfrrange[xpt]:
                for ix in legrange:
                    for sp in range(v["nfsp"]):
                        pb["iipf"][xpt, sp] -= v["fniy"][ix, iycore, 0] * 1.602e-19
                    for gsp in range(v["ngsp"]):
                        pb["igpf"][xpt, gsp] -= v["fngy"][ix, iycore, gsp] * 1.602e-19
            # Wall currents
            for ix in wallrange[xpt]:
                for sp in range(v["nfsp"]):
                    pb["iiwall"][xpt, sp] += v["fniy"][ix, iycore, sp] * 1.602e-19
                for gsp in range(v["ngsp"]):
                    pb["igwall"][xpt, gsp] += v["fngy"][ix, iycore, gsp] * 1.602e-19

            """ Poloidal currents """
            ixi, ixo = v["ixlb"][xpt], v["ixrb"][xpt]
            for iy in range(v["ny"] + 2):
                for sp in range(v["nfsp"]):
                    pb["iirb"][xpt, sp] += v["fnix"][ixo, iy, sp] * 1.602e-19
                    pb["iilb"][xpt, sp] -= v["fnix"][ixi, iy, sp] * 1.602e-19
                for gsp in range(v["ngsp"]):
                    if v["isupgon"][v["ngsp"]] == 0:
                        pb["igrb"][xpt, gsp] += v["fngx"][ixo, iy, gsp] * 1.602e-19
                        pb["iglb"][xpt, gsp] -= v["fngx"][ixi, iy, gsp] * 1.602e-19
                    else:
                        pb["igrb"][xpt, gsp] += v["fnix"][ixo, iy, 1] * 1.602e-19
                        pb["iglb"][xpt, gsp] -= v["fnix"][ixi, iy, 1] * 1.602e-19
        """ Volumetric sources """
        pb["volsor"] = sum(self.get("volpsor"), axis=(0, 1)) * 1.602e-19
        pb["bgsor"] = sum(self.get("psorbgg"), axis=(0, 1)) * 1.602e-19

    def print_particlebalance(self):
        self.particle_balance()
        pb = self.balance["particle"]
        # Set up work arrays
        v = {}
        for var in ["icore", "iplates", "isep", "iwall", "ipf"]:
            v[var] = 0
        for xpt in range(self.get("nxpt")):
            for s in ["i", "g"]:
                v["icore"] += pb[f"i{s}core"][xpt, 0]
                v["isep"] += pb[f"i{s}sep"][xpt, 0]
                v["iwall"] += pb[f"i{s}wall"][xpt, 0]
                v["ipf"] += pb[f"i{s}pf"][xpt, 0]
                for var in ["rb", "lb"]:
                    v["iplates"] += pb[f"i{s}{var}"][xpt, 0]

        print("=" * 30)
        print("=" * 5 + "Particle balance" + "=" * 5)
        print("=" * 30)
        print("Net core hydrogenic flux = {:.3e} A".format(v["icore"]))
        print("Net hydrogen current over separatrix = {:.3e} A".format(v["isep"]))
        print("Net target particle flux = {:.3e} A".format(v["iplates"]))
        print("Net wall particle flux = {:.3e} A".format(v["iwall"]))
        print("Net pf particle flux = {:.3e} A".format(v["ipf"]))
        print("Volumetric particle source = {:.3e} A".format(pb["volsor"][0]))
        print("Background particle source = {:.3e} A".format(pb["bgsor"][0]))

    def xvert(self, arr):
        """ " Returns values of arr on x-vertices (staggered grid)

        index      x-1      x       x+1
            _________________________
        iy  |  ix-1 |   ix  | ix+1  |
            |_______|_______|_______|
        """
        from numpy import zeros_like

        try:
            self.ixp1
        except:
            self.ixp1 = self.get("ixp1")
        retvar = zeros_like(arr)
        retvar[:-1] = 0.5 * (arr[:-1] + arr[1:])
        if self.snull:
            # Account for the X-point cuts
            for ix in [self.ixpt1, self.ixpt2]:
                for iy in range(self.iysptrx + 1):
                    retvar[ix, iy] = 0.5 * (arr[ix, iy] + arr[self.ixp1[ix, iy], iy])
        else:
            raise ValueError("dnull xvert not implemented")
        return retvar

    def dxv(self, arr):
        """Returns differentiaties arr at the vertices"""
        from numpy import zeros

        return
        try:
            self.ixm1
        except:
            self.ixm1 = self.get("ixm1")
        retvar = zeros_like(arr)
        retvar[:-1] = arr[1:] + arr[:-1]
        if self.snull:
            # Account for the X-point cuts
            for ix in [self.ixpt1, self.ixpt2]:
                for iy in range(self.iysptrx + 1):
                    retvar[ix, iy] = 0.5 * (arr[ix, iy] + arr[self.ixp1[ix, iy], iy])
        else:
            raise ValueError("dnull xvert not implemented")
        return retvar

        return

    def dxc(self, arr):
        from numpy import zeros

        """ Returns differentiaties arr at cell centers
        """
        return

    def yvert(self, arr):
        if self.snull:
            1
        else:
            raise ValueError("dnull yvert not implemented")
        return

    def calc_forcebalance(self, cutlo=1e-300):
        """Calculates the force-balance terms"""
        from numpy import minimum, zeros, zeros_like, sum
        from sys import modules

        self.forcebalance = {}

        # Load all variables necessary to the local namespace
        for var in [
            "ev",
            "misotope",
            "natomic",
            "mi",
            "zi",
            "rrv",
            "gpex",
            "gpix",
            "gtex",
            "gtix",
            "pri",
            "netap",
            "qe",
            "fqp",
            "sx",
            "alfe",
            "loglambda",
            "betai",
            "ex",
            "vol",
            "up",
            "volmsor",
            "pondomfpari_use",
        ]:
            setattr(modules[__name__], var, self.get(var))

        # Set up necessary arrays
        den = zeros((misotope, self.get("nchstate")) + self.get("ne").shape)
        gradt = zeros((misotope, self.get("nchstate")) + self.get("ne").shape)
        gradp = zeros((misotope, self.get("nchstate")) + self.get("ne").shape)
        upi = zeros(self.get("ne").shape + (sum(natomic),))
        upi_gradp = zeros(self.get("ne").shape + (sum(natomic),))
        upi_alfe = zeros(self.get("ne").shape + (sum(natomic),))
        upi_betai = zeros(self.get("ne").shape + (sum(natomic),))
        upi_ex = zeros(self.get("ne").shape + (sum(natomic),))
        upi_volmsor = zeros(self.get("ne").shape + (sum(natomic),))
        taudeff = zeros(self.get("ne").shape + (sum(natomic),))

        # Get necessary data
        ni = self.get("ni")
        den[0, 0] = self.xvert(self.get("ne"))
        den[1, 0] = self.xvert(ni[:, :, 0])
        tempa = self.xvert(self.get("te"))
        tif = self.xvert(self.get("ti"))

        # Get flux-limit factor
        ltmax = minimum(
            abs(tempa / (rrv * gtex + cutlo)),
            abs(tif / (rrv * gtix + cutlo)),
            abs(den[0, 0] * tempa / (rrv * gpex + cutlo)),
        )
        # Approx Coulomb mfps
        lmfpe = 1e16 * ((tempa / ev) ** 2 / (den[0, 0] + cutlo))
        lmfpi = 1e16 * ((tif / ev) ** 2 / (den[0, 0] + cutlo))
        # Get ion-pressure gradient scale-lengths
        ltmax = minimum(
            ltmax, abs(self.xvert(pri[:, :, 0]) / (rrv * gpix[:, :, 0] + cutlo))
        )
        # Get flux-limit factor
        flxlimf = 1 / (
            1 + self.get("fricflf") * ((lmfpe + lmfpi) / (ltmax + cutlo)) ** 2
        )
        gradp[0, 0] = rrv * gpex
        gradt[0, 0] = rrv * gtex
        # Get total impurity density
        # TODO: What happens to misotope and natomic when ishymol>0??
        ionspecies = [natomic[x] for x in range(2, misotope)]
        #        dztot = sum(
        #            self.xvert(self.get('ni'))[2:2+sum(ionspecies)],
        #            axis=2
        #        )
        ifld = 0
        # Loop over the different impurity species
        for misa in range(2, misotope):
            # Loop over each impurity species charge state
            for nz in range(natomic[misa]):
                ifld += 1
                # Skip neutral atoms
                ifld += self.get("ziin")[ifld] < 1e-10
                # Calculate the hydrogen-impurity scattering rate
                den[misa, nz] = self.xvert(ni[:, :, ifld])
                zeffv = self.xvert(self.get("zeff"))
                gradt[misa, nz] = rrv * gtix
                gradp[misa, nz] = rrv * gpix[:, :, ifld] - pondomfpari_use[:, :, ifld]
                if self.get("is_z0_imp_const") == 0:
                    z0 = den[0, 0] * zeffv / (den[1, 0] + cutlo) - 1
                else:
                    z0 = z0_imp_const
                taud = (
                    self.get("cftaud")
                    * 5.624e54
                    * mi[0] ** 0.5
                    * mi[ifld]
                    * tif**1.5
                    / (
                        loglambda * den[misa, nz] * zi[ifld] ** 2 * (mi[0] + mi[ifld])
                        + cutlo
                    )
                )
                taudeff[:, :, ifld] = (
                    flxlimf
                    * taud
                    * den[misa, nz]
                    * (1 + 2.65 * z0)
                    * (1 + 0.285 * z0)
                    / (den[0, 0] * (1 + 0.24 * z0) * (1 + 0.93 * z0) + cutlo)
                )

                # Store the components of the force-balance equation
                upi_gradp[:, :, ifld] = -gradp[misa, nz] / (den[misa, nz] + cutlo)
                upi_gradp[:, :, ifld] *= taudeff[:, :, ifld] / mi[0]
                upi_alfe[:, :, ifld] = alfe[ifld] * gradt[0, 0]
                upi_alfe[:, :, ifld] *= taudeff[:, :, ifld] / mi[0]
                upi_betai[:, :, ifld] = betai[ifld] * gradt[misa, nz]
                upi_betai[:, :, ifld] *= taudeff[:, :, ifld] / mi[0]
                upi_ex[:, :, ifld] = qe * zi[ifld] * rrv * ex
                upi_ex[:, :, ifld] *= taudeff[:, :, ifld] / mi[0]
                upi_volmsor[:, :, ifld] = volmsor[:, :, ifld] / (
                    den[misa, nz] * vol + cutlo
                )
                upi_volmsor[:, :, ifld] *= taudeff[:, :, ifld] / mi[0]
                # Solve force-balance equation for impurity velocity
                upi[:, :, ifld] = (
                    up[:, :, 0]
                    + upi_gradp[:, :, ifld]
                    + upi_alfe[:, :, ifld]
                    + upi_betai[:, :, ifld]
                    + upi_ex[:, :, ifld]
                    + upi_volmsor[:, :, ifld]
                )

        self.forcebalance["upi"] = upi
        self.forcebalance["up"] = up[:, :, 0]
        self.forcebalance["upi_gradp"] = upi_gradp
        self.forcebalance["upi_alfe"] = upi_alfe
        self.forcebalance["upi_betai"] = upi_betai
        self.forcebalance["upi_ex"] = upi_ex
        self.forcebalance["taudeff"] = taudeff
        self.forcebalance["upi_volmsor"] = upi_volmsor

        return upi, self.forcebalance

    def pradpltwl(self):
        from numpy import zeros, pi, cos
        from math import atan2

        ny = self.get("ny")
        nx = self.get("nx")
        nxpt = self.get("nxpt")
        ixlb = self.get("ixlb")
        ixrb = self.get("ixrb")
        rm = self.get("rm")
        zm = self.get("zm")
        sx = self.get("sx")
        angfx = self.get("angfx")
        vol = self.get("vol")
        eeli = self.get("eeli")
        ebind = self.get("ebind")
        ev = self.get("ev")
        psor = self.get("psor")
        erlrc = self.get("erlrc")
        isimpon = self.get("isimpon")
        # Initialize arrays
        self.pwr_pltz = zeros((ny + 2, 2 * nxpt))
        self.pwr_plth = zeros((ny + 2, 2 * nxpt))
        self.pwr_wallz = zeros((nx + 2))
        self.pwr_wallh = zeros((nx + 2))
        self.pwr_pfwallz = zeros(((nx + 2) * nxpt))
        self.pwr_pfwallh = zeros(((nx + 2) * nxpt))
        if isimpon > 0:
            prdu = self.get("prad")
        else:
            prdu = zeros((nx + 2, ny + 2))
        nj = self.get("nxomit")
        for ip in range(0, 2 * nxpt):
            ixv = (1 - (ip % 2)) * ixlb[0] + (ip % 2) * (ixrb[0] + 1)
            print(ixv)
            for iyv in range(1, ny + 1):
                for iy in range(1, ny + 1):
                    for ix in range(1, nx + 1):
                        theta_ray1 = atan2(
                            zm[ixv + nj, iyv, 1] - zm[ix + nj, iy, 0],
                            rm[ixv + nj, iyv, 1] - rm[ix + nj, iy, 0],
                        )
                        theta_ray2 = atan2(
                            zm[ixv + nj, iyv, 3] - zm[ix + nj, iy, 0],
                            rm[ixv + nj, iyv, 3] - rm[ix + nj, iy, 0],
                        )
                        if (ix == 10) and (iy == 10) and (iyv == 10):
                            print(theta_ray1, theta_ray2)
                        dthgy = abs(theta_ray1 - theta_ray2)
                        frth = min(dthgy, 2 * pi - dthgy) / (2 * pi)
                        sxo = sx[ixv, iyv] / cos(angfx[ixv, iyv])
                        if (ix == 10) and (iy == 10) and (iyv == 10):
                            print(dthgy, frth, sxo)
                        self.pwr_pltz[iyv, ip] += (
                            prdu[ix, iy] * vol[ix, iy] * frth / sxo
                        )
                        self.pwr_plth[iyv, ip] += (
                            (
                                (eeli[ix, iy] - ebind * ev) * psor[ix, iy, 0]
                                + erlrc[ix, iy]
                            )
                            * frth
                            / sxo
                        )
        self.pwr_pltz[0, ip] = self.pwr_pltz[1, ip]
        self.pwr_pltz[-1, ip] = self.pwr_pltz[-2, ip]
        self.pwr_plth[0, ip] = self.pwr_plth[1, ip]
        self.pwr_plth[-1, ip] = self.pwr_plth[-2, ip]
