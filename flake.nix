{
  description = "Mini-Coding-Agent: a small standalone coding agent backed by Ollama";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python3; # project needs Python 3.10+ and only the stdlib

        mini-coding-agent = pkgs.stdenv.mkDerivation {
          pname = "mini-coding-agent";
          version = "0.1.0";
          src = ./.;

          dontBuild = true;
          nativeBuildInputs = [ pkgs.makeWrapper ];

          installPhase = ''
            runHook preInstall
            install -Dm644 mini_coding_agent.py \
              $out/lib/mini-coding-agent/mini_coding_agent.py
            makeWrapper ${python}/bin/python $out/bin/mini-coding-agent \
              --add-flags $out/lib/mini-coding-agent/mini_coding_agent.py \
              --prefix PATH : ${pkgs.lib.makeBinPath [ pkgs.git ]}
            runHook postInstall
          '';

          meta = {
            description = "Minimal local coding agent loop using Ollama";
            mainProgram = "mini-coding-agent";
          };
        };
      in
      {
        packages = {
          default = mini-coding-agent;
          inherit mini-coding-agent;
        };

        apps.default = flake-utils.lib.mkApp { drv = mini-coding-agent; };

        devShells.default = pkgs.mkShell {
          packages = [
            python
            pkgs.uv
            pkgs.git
            pkgs.ollama
          ];
          shellHook = ''
            echo "mini-coding-agent dev shell"
            echo "  ollama serve                 # in another terminal"
            echo "  ollama pull qwen3.5:4b"
            echo "  python mini_coding_agent.py"
          '';
        };
      });
}
