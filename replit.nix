{ pkgs }: {
  deps = [
    pkgs.python310Packages.flask  # 使用 python310Packages
    pkgs.python310Packages.flask_cors
    pkgs.python310Packages.transformers
    pkgs.cacert
  ];
}