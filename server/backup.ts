import { backup } from 'node:sqlite';
import { mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { openDatabase } from './database.js';
import { configFromEnvironment } from './config.js';
const config=configFromEnvironment();const directory=process.env.BACKUP_DIR||'backups';mkdirSync(directory,{recursive:true});
const path=join(directory,`codey-${new Date().toISOString().replace(/[:.]/g,'-')}.sqlite`);
const db=openDatabase(config.databasePath);await backup(db,path);db.close();console.log('Consistent SQLite backup saved to '+path);
