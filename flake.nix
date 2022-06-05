{
  description = "A flake to run pridefetch";

  inputs = {
    nixpkgs-master.url = "github:nixos/nixpkgs/nixpkgs-unstable";
  };

  outputs = { self, nixpkgs, nixpkgs-master }: let
    system = "x86_64-linux";
 
    forAllSystems = f: nixpkgs.lib.genAttrs nixpkgs.lib.systems.supported.hydra (system: f system);
  in rec {
    packages = forAllSystems (system: let 
      pkgs = import nixpkgs {
        inherit system;
      };
      pkgs-master = import nixpkgs-master {
        inherit system;
      };
    in {
      pridefetch = pkgs-master.pridefetch.overrideAttrs (finalAttrs: previousAttrs: {
        src = builtins.path { path = ./.; name = "pridefetch"; };
      });
    });

    defaultPackage = forAllSystems (system: self.packages.${system}.pridefetch);
  };
}
