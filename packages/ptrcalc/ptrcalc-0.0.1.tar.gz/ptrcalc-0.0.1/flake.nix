{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };
  outputs = { self, nixpkgs, ... }: {
    packages.x86_64-linux = let
      pkgs = import nixpkgs {
        system = "x86_64-linux";
      };
    in {
      ptrcalc = pkgs.python311Packages.buildPythonPackage rec {
        pname = "ptrcalc";
        version = "0.0.1";

        src = ./.;

        format = "pyproject";

        buildInputs = [ pkgs.python311Packages.hatchling ];
        propagatedBuildInputs = with pkgs.python311Packages; [
        ];

        pythonImportsCheck = [ "ptrcalc" ];
      };
      default = self.packages.x86_64-linux.ptrcalc;
    };

    hydraJobs = {
      inherit (self)
        packages;
    };
  };
}
