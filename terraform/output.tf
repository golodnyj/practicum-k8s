output "cluster_id" {
  value = yandex_mdb_postgresql_cluster.lab-postgresql.id
}

output "database_uri" {
  value = local.dburi
}

output "database_hosts" {
  value = join(",", local.dbhosts)
}

