
path = 'templates/careers/career_detail.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i in range(len(lines)):
    if skip:
        skip = False
        continue
        
    line = lines[i]
    stripped = line.strip()
    
    # Check for split tags
    if (stripped.endswith('|upper') or stripped.endswith('pluralize') or stripped.endswith('date:"M d, Y"')) and \
       i + 1 < len(lines) and lines[i+1].strip().startswith('}}'):
        
        # Join with the next line, removing extra whitespace
        next_line = lines[i+1].strip()
        combined = line.rstrip() + ' ' + next_line + '\n'
        new_lines.append(combined)
        skip = True # Skip the next line since we merged it
    elif stripped.endswith('{{') and i + 1 < len(lines) and 'review.created_at' in lines[i+1]:
         # Handle the split {{ review.created_at case
        next_line = lines[i+1].strip()
        combined = line.rstrip() + ' ' + next_line
        # Check if it continues to a third line
        if combined.strip().endswith('}}'):
             new_lines.append(combined + '\n')
             skip = True
        else:
             # Just append and hope? No, let's just use the simpler logic above since the split I saw was different
             new_lines.append(line)
    else:
        new_lines.append(line)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Fixed template file using line iteration")
