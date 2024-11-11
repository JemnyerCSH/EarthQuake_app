{ pkgs }: {
  deps = [
    pkgs.python310Packages.flask
    pkgs.python310Packages.flask_cors
    pkgs.python310Packages.transformers
    pkgs.cacert
  ];
}