{
  description = "A flake to run pridefetch";

  inputs = {
    nixpkgs-unstable.url = "github:nixos/nixpkgs/nixpkgs-unstable";
  };

  outputs = { self, nixpkgs, nixpkgs-unstable }: let
    system = "x86_64-linux";

    forAllSystems = f: nixpkgs.lib.genAttrs nixpkgs.lib.platforms.all (system: f system);
  in rec {
    packages = forAllSystems (system: let
      pkgs = import nixpkgs {
        inherit system;
      };
      pkgs-unstable = import nixpkgs-unstable {
        inherit system;
      };
    in {
      pridefetch = pkgs-unstable.pridefetch.overrideAttrs (finalAttrs: previousAttrs: {
        src = builtins.path { path = ./.; name = "pridefetch"; };
      });
    });

    defaultPackage = forAllSystems (system: self.packages.${system}.pridefetch);
  };
}
