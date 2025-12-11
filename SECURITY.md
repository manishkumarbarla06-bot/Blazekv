# Security Guide for BlazeKV

## Table of Contents
1. [GitHub Account Security](#github-account-security)
2. [Local Data Protection](#local-data-protection)
3. [Git & Credential Management](#git--credential-management)
4. [Repository Security](#repository-security)
5. [Incident Response](#incident-response)

---

## GitHub Account Security

### Essential Steps to Protect Your Account

#### 1. Enable Two-Factor Authentication (2FA)
- **Why**: Prevents unauthorized access even if password is compromised
- **Steps**:
  1. Go to https://github.com/settings/security
  2. Click "Enable two-factor authentication"
  3. Choose authenticator app (Microsoft Authenticator, Google Authenticator, or Authy)
  4. Save recovery codes in a secure location
  5. Add backup phone numbers

#### 2. Set Up SSH Keys (Recommended)
- **Why**: Better than HTTPS passwords; can't be phished
- **Generate key** (run in PowerShell):
  ```powershell
  ssh-keygen -t ed25519 -C "your_email@example.com"
  ```
- **Add to GitHub**:
  1. Copy public key: `cat ~/.ssh/id_ed25519.pub`
  2. Go to https://github.com/settings/keys
  3. Click "New SSH key"
  4. Paste and save
- **Configure Git**:
  ```powershell
  git config --global user.email "your_email@example.com"
  git config --global user.name "Your Name"
  ```

#### 3. Configure GitHub Personal Access Tokens (PAT)
- **For automated tools** (CI/CD, npm, PyPI):
  1. Go to https://github.com/settings/tokens (classic) or https://github.com/settings/personal-access-tokens/new (fine-grained)
  2. Create token with **minimum required permissions**
  3. Set expiration date (max 1 year)
  4. **Never commit** tokens to repository
  5. Store in environment variables or GitHub Secrets
- **Never share** tokens in emails, messages, or code

#### 4. Review Active Sessions
- **Weekly**:
  1. Go to https://github.com/settings/sessions
  2. Review and revoke unknown devices
  3. Check for unusual locations or timestamps

---

## Local Data Protection

### 1. Backup Your Data Locally
- **Create automated backups** of `data.db`:
  ```powershell
  # Create backup folder
  mkdir "$env:USERPROFILE\BlazeKV_Backups"
  
  # Create scheduled backup script (backup.ps1)
  $source = "c:\flutterapps\habit_tracker\documents\projects\blazekv\data.db"
  $dest = "$env:USERPROFILE\BlazeKV_Backups\data_$(Get-Date -Format 'yyyy-MM-dd_HH-mm-ss').db"
  Copy-Item $source $dest -ErrorAction SilentlyContinue
  Get-ChildItem "$env:USERPROFILE\BlazeKV_Backups" | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-30)} | Remove-Item
  ```

### 2. Encrypt Sensitive Data
- **Never store passwords in `data.db`**
- **Use hashing** for sensitive values:
  ```powershell
  # Example: Hash password with SHA-256
  $password = "your_password"
  $hash = [System.Security.Cryptography.SHA256]::Create().ComputeHash([System.Text.Encoding]::UTF8.GetBytes($password))
  [System.BitConverter]::ToString($hash)
  ```

### 3. Control File Permissions
- **Restrict `data.db` access**:
  ```powershell
  # Windows: Set file permissions
  icacls "c:\flutterapps\habit_tracker\documents\projects\blazekv\data.db" /grant:r "$env:USERNAME:(F)" /inheritance:r
  ```

### 4. Regular Backup to Cloud (Optional but Recommended)
- **Use OneDrive, Google Drive, or Dropbox**:
  1. Place backup folder in cloud-synced directory
  2. Enable version history
  3. Test restores monthly

---

## Git & Credential Management

### 1. Configure Git Safely
```powershell
# Store credentials securely (Windows Credential Manager)
git config --global credential.helper wincred

# Or use SSH (recommended)
git config --global core.sshcommand "ssh -i $env:USERPROFILE\.ssh\id_ed25519"
```

### 2. Prevent Accidental Secret Commits
- **Update `.gitignore`** to exclude sensitive files:
  ```
  # Sensitive files
  .env
  .env.local
  .env.*.local
  secrets.txt
  *.key
  *.pem
  data.db
  node_modules/
  *.log
  ```

- **Install git hooks** (pre-commit checks):
  Create `.git/hooks/pre-commit`:
  ```bash
  #!/bin/bash
  # Check for common secrets
  if git diff --cached | grep -E "(password|secret|token|key|api_key)" > /dev/null; then
    echo "ERROR: Potential secret found in commit!"
    echo "Please remove sensitive data before committing"
    exit 1
  fi
  ```

### 3. Review Commits Before Pushing
```powershell
# Always review what you're pushing
git log --oneline -5          # See last 5 commits
git log -p origin/main..main  # See diff of unpushed commits
git status                    # Verify staging area
```

### 4. Use Signed Commits (Optional but Recommended)
```powershell
# Configure GPG signing
git config --global commit.gpgsign true
git config --global user.signingkey <GPG_KEY_ID>

# Or use SSH signing (easier)
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
```

---

## Repository Security

### 1. Branch Protection Rules
- **Protect `main` branch**:
  1. Go to https://github.com/manishkumarbarla06-bot/Blazekv/settings/branches
  2. Click "Add rule"
  3. Pattern: `main`
  4. Enable:
     - ✅ Require pull request reviews (1-2 reviewers)
     - ✅ Require status checks to pass
     - ✅ Require branches to be up to date before merging
     - ✅ Dismiss stale pull request approvals
     - ✅ Include administrators

### 2. Code Scanning
- **Enable GitHub's security scanning**:
  1. Go to https://github.com/manishkumarbarla06-bot/Blazekv/security
  2. Enable "Dependabot alerts"
  3. Enable "Code scanning"
  4. Enable "Secret scanning"

### 3. Manage Collaborators & Teams
- **Review access**:
  1. Go to https://github.com/manishkumarbarla06-bot/Blazekv/settings/access
  2. Remove users no longer needing access
  3. Use minimum required permissions (read < triage < write < maintain < admin)

### 4. Repository Settings
- **Security best practices**:
  1. Disable "Allow force pushes" on main
  2. Disable "Allow deletions" on main
  3. Enable "Automatic delete head branches"
  4. Set default branch to `main`

---

## Secrets Management

### 1. GitHub Secrets (for CI/CD)
- **Add secrets** at https://github.com/manishkumarbarla06-bot/Blazekv/settings/secrets/actions
- **Never log secrets** in workflows
- **Rotate regularly** (every 90 days)

**Example: Secure PyPI publishing**
```yaml
# .github/workflows/publish.yml
- name: Publish to PyPI
  env:
    PYPI_TOKEN: ${{ secrets.PYPI_TOKEN }}
  run: |
    python -m twine upload dist/* -u __token__ -p $PYPI_TOKEN
```

### 2. Local Secrets (.env file)
```powershell
# Create .env in project root (NEVER commit)
$env:PYPI_TOKEN = "your_token"
$env:GITHUB_TOKEN = "your_token"

# Load in script
$env:PYPI_TOKEN = (Get-Content .env | Select-String "PYPI_TOKEN" | ForEach-Object {$_.ToString().Split('=')[1]})
```

### 3. Rotate Secrets Regularly
- **90-day rotation policy**:
  - Mark calendar reminders
  - Create new token
  - Update GitHub Secrets
  - Delete old token from GitHub
  - Test in CI before deletion

---

## Monitoring & Alerts

### 1. GitHub Email Notifications
- Go to https://github.com/settings/notifications
- Enable alerts for:
  - ✅ "Repository security and analysis"
  - ✅ "Dependabot alerts"
  - ✅ "Dependabot security updates"

### 2. Audit Log Review (Weekly)
```powershell
# Use GitHub API to check recent activity
curl -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/repos/manishkumarbarla06-bot/Blazekv/events
```

### 3. Set Up Security Alerts
- Go to https://github.com/manishkumarbarla06-bot/Blazekv/security/alerts
- Review findings regularly
- Fix vulnerabilities promptly

---

## Incident Response

### If You Suspect Compromised Credentials

**Immediate Actions (within 30 minutes)**:
1. Go to https://github.com/settings/security
2. Change password immediately
3. Revoke all active sessions
4. Revoke compromised personal access tokens
5. Rotate SSH keys

**Follow-up Actions**:
1. Review recent commits: `git log --oneline -20`
2. Check push history: `git reflog`
3. Audit repository settings and collaborators
4. Review GitHub Actions runs for unauthorized usage
5. Check for any force pushes or deletions
6. If code was exposed, notify any users of the project

### If Data.db Was Exposed
1. Stop BlazeKV application
2. Backup exposed `data.db`
3. Delete or wipe `data.db`
4. Create new clean database
5. Audit for unauthorized data access
6. Notify any users about the incident

### If Repository Was Compromised
1. Do NOT delete the repository
2. Create new branch from known-good commit:
   ```powershell
   git branch safe-recovery <last-safe-commit-hash>
   git push origin safe-recovery
   ```
3. Contact GitHub Support at https://support.github.com
4. Retain logs for investigation

---

## Checklist: Monthly Security Review

- [ ] Check GitHub sessions for unknown devices
- [ ] Review repository collaborators and access levels
- [ ] Check for unresolved Dependabot alerts
- [ ] Verify branch protection rules are enabled
- [ ] Test backup restoration
- [ ] Review recent commits and pushes
- [ ] Rotate API tokens/secrets (if 90+ days old)
- [ ] Check GitHub Actions for unauthorized changes
- [ ] Verify SSH keys are still needed
- [ ] Review GitHub audit log

---

## Resources

- **GitHub Security Documentation**: https://docs.github.com/en/code-security
- **GitHub Security Advisories**: https://github.com/advisories
- **NIST Cybersecurity Framework**: https://www.nist.gov/cyberframework
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **Password Manager Recommendations**: Bitwarden, 1Password, LastPass
- **Two-Factor Authentication Apps**: Microsoft Authenticator, Google Authenticator, Authy

---

## Support

If you experience a security issue:
1. **Do NOT disclose publicly** on issues/PRs
2. **Use GitHub Security Advisory**: https://github.com/manishkumarbarla06-bot/Blazekv/security/advisories
3. **Contact maintainer privately**
4. **Allow 90 days** for a fix before disclosure

---

**Last Updated**: December 11, 2025  
**Document Version**: 1.0  
**Security Level**: Public (Safe to share)
