# GitHub and Account Security Setup Guide for BlazeKV

## Quick Start Security Checklist

### 1. GitHub Two-Factor Authentication (2FA) ⭐ CRITICAL
- [ ] Visit https://github.com/settings/security
- [ ] Click "Enable two-factor authentication"
- [ ] Choose authenticator app (Google Authenticator, Microsoft Authenticator, or Authy)
- [ ] **Save recovery codes in a secure location** (offline, password manager, etc.)
- [ ] Test login with 2FA enabled

**Why**: Prevents account takeover even if password is leaked

### 2. SSH Keys (Recommended over HTTPS)
- [ ] Generate SSH key:
  ```powershell
  ssh-keygen -t ed25519 -C "your_email@example.com"
  # Press Enter for all prompts to use defaults
  ```
- [ ] Add to GitHub:
  1. Copy key: `cat $env:USERPROFILE\.ssh\id_ed25519.pub`
  2. Go to https://github.com/settings/keys
  3. Click "New SSH key"
  4. Paste and save
- [ ] Configure git to use SSH:
  ```powershell
  git config --global core.sshcommand "ssh -i $env:USERPROFILE\.ssh\id_ed25519"
  ```

**Why**: SSH keys can't be phished; stronger than passwords

### 3. Protect Your Access Tokens
- [ ] Never create personal access tokens unless absolutely necessary
- [ ] If you need one:
  1. Go to https://github.com/settings/tokens
  2. Click "Generate new token"
  3. Select **minimum required** scopes
  4. Set **short expiration** (7-30 days)
  5. Store in GitHub Secrets, NOT in code
- [ ] Tokens = passwords; never share or commit them

**Why**: Tokens are keys to your account; minimal scope = minimal damage if leaked

### 4. Protect Local data.db
- [ ] Make backup of `data.db`:
  ```powershell
  Copy-Item "c:\flutterapps\habit_tracker\documents\projects\blazekv\data.db" `
    "$env:USERPROFILE\BlazeKV_Backups\data_backup.db"
  ```
- [ ] Restrict file permissions:
  ```powershell
  icacls "c:\flutterapps\habit_tracker\documents\projects\blazekv\data.db" `
    /grant:r "$env:USERNAME:(F)" /inheritance:r
  ```
- [ ] Add to `.gitignore` (already done):
  ```
  data.db
  ```

**Why**: Ensures only you can access sensitive data; backup prevents data loss

### 5. Set Up Automated Backups
- [ ] Run backup script weekly:
  ```powershell
  # First run
  & "c:\flutterapps\habit_tracker\documents\projects\blazekv\scripts\backup.ps1"
  
  # Schedule daily (Windows Task Scheduler)
  $trigger = New-ScheduledTaskTrigger -Daily -At "02:00 AM"
  $action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-File 'c:\flutterapps\habit_tracker\documents\projects\blazekv\scripts\backup.ps1'"
  Register-ScheduledTask -TaskName "BlazeKV-Daily-Backup" `
    -Trigger $trigger -Action $action -RunLevel Highest
  ```

**Why**: Automated backups mean you never lose data due to accidents or attacks

### 6. Review GitHub Sessions
- [ ] Weekly check:
  1. Go to https://github.com/settings/sessions
  2. Look for unfamiliar devices/locations
  3. Revoke any suspicious sessions

**Why**: Detects if someone else accessed your account

### 7. Install Pre-Commit Hook
- [ ] Copy hook to git:
  ```powershell
  Copy-Item "scripts\pre-commit-hook.sh" ".git\hooks\pre-commit"
  # On Windows, you might need to use Git Bash or WSL for this
  ```
- [ ] Test it:
  ```powershell
  # Try to commit a fake secret (this should be blocked)
  echo "test_password_123" >> test.txt
  git add test.txt
  git commit -m "test"  # Should be blocked
  ```

**Why**: Prevents accidental secret commits before they reach GitHub

---

## What NOT to Do ❌

1. **Never commit passwords, API keys, or tokens**
   - Not even with "DO NOT USE" comments
   - Not in example files
   - Not in test data

2. **Never use same password for multiple accounts**
   - Use password manager (Bitwarden, 1Password, LastPass)
   - Generate unique passwords for GitHub, PyPI, Patreon, etc.

3. **Never share your SSH private key**
   - Keep `~/.ssh/id_ed25519` offline
   - Only share public keys (`id_ed25519.pub`)

4. **Never write credentials in code**
   - Use environment variables
   - Use `.env` files (excluded from git)
   - Use GitHub Secrets for CI/CD

5. **Never accept untrusted code**
   - Review all pull requests carefully
   - Run security scans on dependencies

---

## Recovery Steps If Compromised 🚨

### If Your GitHub Password is Leaked:
1. **Immediately**:
   ```powershell
   # Change password at https://github.com/settings/account
   ```
2. **Within 1 hour**:
   - Go to https://github.com/settings/sessions
   - Revoke all active sessions except current
3. **Within 24 hours**:
   - Rotate all PATs (delete old ones)
   - Rotate SSH keys

### If API Token is Leaked:
1. **Delete immediately** at https://github.com/settings/tokens
2. **Search repository** for any commits using it:
   ```powershell
   git log -p | Select-String "token_that_was_leaked"
   ```
3. **If found**: Contact GitHub Support (not fixable without professional help)

### If SSH Private Key is Leaked:
1. **Delete from** `~/.ssh/id_ed25519`
2. **Generate new key** and add to GitHub
3. **Remove old key** from https://github.com/settings/keys

### If data.db is Exposed:
1. **Stop using** that database file
2. **Delete it** (or keep for forensics if compromised)
3. **Create fresh** database
4. Notify any users who might be affected

---

## Monitoring & Maintenance 📊

### Weekly Tasks:
- [ ] Review GitHub sessions for unknown devices
- [ ] Check for failed login attempts in email

### Monthly Tasks:
- [ ] Review repository collaborators
- [ ] Check for unresolved security alerts
- [ ] Test backup restoration
- [ ] Verify branch protection is still enabled

### Quarterly Tasks:
- [ ] Rotate API tokens (if not auto-rotating)
- [ ] Audit commit history for accidental leaks:
  ```powershell
  git log --all -p | Select-String "password|token|secret|key"
  ```
- [ ] Update security documentation

### Annually:
- [ ] Security audit of entire codebase
- [ ] Review and update security policies
- [ ] Check for deprecated libraries/tools

---

## Useful Commands Reference

```powershell
# Check git configuration
git config --list

# View your SSH keys
ls $env:USERPROFILE\.ssh\

# Check for uncommitted secrets
git diff | Select-String "password|token|secret|key" -Pattern "^\+"

# View commit history (including deleted branches)
git reflog

# List all branches and commits
git log --oneline --all --graph

# Check which files are ignored
git check-ignore -v *

# Verify no large files committed
git ls-files --long | Sort-Object -Property {[int]$_[50..]} -Descending | Select-Object -First 10
```

---

## Resources

- **GitHub Security Documentation**: https://docs.github.com/en/code-security
- **GitHub Security Best Practices**: https://docs.github.com/en/code-security/secret-scanning
- **NIST Cybersecurity Framework**: https://www.nist.gov/cyberframework
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **Recommended Password Managers**:
  - Bitwarden (free & open-source)
  - 1Password (paid)
  - LastPass (free tier available)

---

## Support & Incidents

If you suspect a security breach:
1. **Don't panic** - most issues can be contained quickly
2. **Don't commit** anything else to the repo
3. **Document** what you noticed and when
4. **Report** to GitHub Support: https://support.github.com
5. **Rotate** all credentials immediately

---

**Last Updated**: December 11, 2025  
**Document Version**: 1.0  
**Keep This Safe**: Yes - This contains critical security information
