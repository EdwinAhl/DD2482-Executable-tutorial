# Allow reading secrets under "secret/"
path "secret/*" {
  capabilities = ["read", "list"]
}