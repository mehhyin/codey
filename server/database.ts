import { DatabaseSync } from 'node:sqlite';
import { mkdirSync } from 'node:fs';
import { dirname } from 'node:path';

export function openDatabase(path:string){
  if(path!==':memory:')mkdirSync(dirname(path),{recursive:true});
  const db=new DatabaseSync(path);
  db.exec('PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;');
  return db;
}
export function migrateProgress(db:DatabaseSync){
  db.exec(`
    CREATE TABLE IF NOT EXISTS app_migration(version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS workspace(
      user_id TEXT PRIMARY KEY REFERENCES user(id) ON DELETE CASCADE,
      last_exercise TEXT, imported_at TEXT, updated_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS draft(
      user_id TEXT NOT NULL REFERENCES user(id) ON DELETE CASCADE,
      exercise_id TEXT NOT NULL, files_json TEXT NOT NULL, revision INTEGER NOT NULL DEFAULT 1,
      updated_at TEXT NOT NULL, PRIMARY KEY(user_id,exercise_id)
    );
    CREATE TABLE IF NOT EXISTS exercise_progress(
      user_id TEXT NOT NULL REFERENCES user(id) ON DELETE CASCADE,
      exercise_id TEXT NOT NULL, hints INTEGER NOT NULL DEFAULT 0,
      completed_at TEXT, completion_source TEXT, solution_revealed_at TEXT,
      PRIMARY KEY(user_id,exercise_id)
    );
    CREATE TABLE IF NOT EXISTS attempt(
      id TEXT PRIMARY KEY,user_id TEXT NOT NULL REFERENCES user(id) ON DELETE CASCADE,
      exercise_id TEXT NOT NULL, files_json TEXT NOT NULL,result_json TEXT NOT NULL,
      passed INTEGER NOT NULL, source TEXT NOT NULL,created_at TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS attempt_user_exercise ON attempt(user_id,exercise_id,created_at DESC);
    INSERT OR IGNORE INTO app_migration(version,applied_at) VALUES(1,datetime('now'));
  `);
}
export function transaction<T>(db:DatabaseSync,fn:()=>T):T{
  db.exec('BEGIN IMMEDIATE');
  try{const value=fn();db.exec('COMMIT');return value;}
  catch(error){db.exec('ROLLBACK');throw error;}
}
