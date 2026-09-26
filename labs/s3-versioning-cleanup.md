# S3 Versioning and Cleanup Lab

## Objective

Demonstrate Amazon S3 object versioning, version management, Delete Markers, object recovery, permanent deletion, and resource cleanup using the AWS CLI.

## Environment

- AWS Service: Amazon S3
- Region: ap-south-1 (Mumbai)
- Bucket: kabir-aws-learning-s3-2026
- Object: aws-s3-test.txt
- Tool: AWS CLI
- OS: Windows PowerShell

---

## 1. Create the S3 Bucket

``powershell
aws s3 mb s3://kabir-aws-learning-s3-2026 --region ap-south-1
``

Result:

``text
make_bucket: kabir-aws-learning-s3-2026
``

The bucket was created successfully in the Mumbai region.

## 2. Verify the Bucket

``powershell
aws s3 ls
``

The newly created bucket appeared in the S3 bucket listing.

## 3. Create a Test Object

``powershell
"AWS S3 Versioning Test" | Out-File aws-s3-test.txt
``

## 4. Upload the Object

``powershell
aws s3 cp .\aws-s3-test.txt s3://kabir-aws-learning-s3-2026/
``

## 5. Verify the Uploaded Object

``powershell
aws s3 ls s3://kabir-aws-learning-s3-2026/
``

The object ws-s3-test.txt was successfully displayed.

## 6. Enable S3 Versioning

``powershell
aws s3api put-bucket-versioning ` 
  --bucket kabir-aws-learning-s3-2026 ` 
  --versioning-configuration Status=Enabled
``

Verify:

``powershell
aws s3api get-bucket-versioning ` 
  --bucket kabir-aws-learning-s3-2026
``

Expected result:

``json
{
    "Status": "Enabled"
}
``

## 7. Create Multiple Object Versions

The test object was modified and uploaded multiple times, creating three object versions during the exercise.

### Version 3

Final test content:

``text
Version 3 - Final AWS S3 Test
``

Latest Version ID recorded:

``text
WhkLLM_36Jya8cxPlzW75kKfuRlDJVw5
``

Version 2 ID recorded:

``text
KlEPkP6h.cgeoqLwNOKZSfj82icGG656
``

The original object created before Versioning was enabled had the special Version ID:

``text
null
``

## 8. Verify the Current Object Version

``powershell
aws s3api head-object ` 
  --bucket kabir-aws-learning-s3-2026 ` 
  --key aws-s3-test.txt
``

The response confirmed Version 3:

``text
VersionId: WhkLLM_36Jya8cxPlzW75kKfuRlDJVw5
``

The object also showed server-side encryption using AES256.

## 9. Create an S3 Delete Marker

A normal object deletion was performed:

``powershell
aws s3api delete-object ` 
  --bucket kabir-aws-learning-s3-2026 ` 
  --key aws-s3-test.txt
``

Because Versioning was enabled, the delete operation created a Delete Marker.

Delete Marker ID:

``text
GW2YW2AmC7isJrrcKeShvlsZZcxB_JUf
``

## 10. Verify Delete Marker Behavior

After the Delete Marker was created:

``powershell
aws s3api head-object ` 
  --bucket kabir-aws-learning-s3-2026 ` 
  --key aws-s3-test.txt
``

The command returned HTTP 404 Not Found because the current version was a Delete Marker.

## 11. List Versions and Delete Markers

``powershell
aws s3api list-object-versions ` 
  --bucket kabir-aws-learning-s3-2026 ` 
  --prefix aws-s3-test.txt ` 
  --output json
``

The listing identified the object versions and the Delete Marker.

## 12. Remove the Delete Marker

``powershell
aws s3api delete-object ` 
  --bucket kabir-aws-learning-s3-2026 ` 
  --key aws-s3-test.txt ` 
  --version-id GW2YW2AmC7isJrrcKeShvlsZZcxB_JUf
``

After removing the Delete Marker, Version 3 became visible again.

## 13. Permanently Delete Version 2

``powershell
aws s3api delete-object ` 
  --bucket kabir-aws-learning-s3-2026 ` 
  --key aws-s3-test.txt ` 
  --version-id KlEPkP6h.cgeoqLwNOKZSfj82icGG656
``

Version 2 was permanently removed.

## 14. Understand the 
ull Version

The remaining 
ull Version ID represented the object created before S3 Versioning was enabled.

This is an important S3 versioning behavior when performing object cleanup.

## 15. Permanently Delete the 
ull Version

``powershell
aws s3api delete-object ` 
  --bucket kabir-aws-learning-s3-2026 ` 
  --key aws-s3-test.txt ` 
  --version-id "null"
``

## 16. Verify Complete Object Cleanup

``powershell
aws s3api list-object-versions ` 
  --bucket kabir-aws-learning-s3-2026 ` 
  --prefix aws-s3-test.txt ` 
  --output json
``

The final response contained no object versions or Delete Markers.

The bucket was also checked:

``powershell
aws s3 ls s3://kabir-aws-learning-s3-2026/
``

No objects remained.

## 17. Verify Bucket Existence

``powershell
aws s3api head-bucket ` 
  --bucket kabir-aws-learning-s3-2026
``

The bucket was confirmed in p-south-1.

## 18. Delete the Empty Bucket

``powershell
aws s3 rb s3://kabir-aws-learning-s3-2026
``

Result:

``text
remove_bucket: kabir-aws-learning-s3-2026
``

## 19. Final Verification

``powershell
aws s3 ls
``

The deleted bucket no longer appeared.

# Key Learning Outcomes

## S3 Versioning

Versioning allows multiple versions of the same object to coexist.

Deleting the current object while Versioning is enabled normally creates a Delete Marker instead of permanently removing previous versions.

## Delete Markers

A Delete Marker makes the object appear deleted through the normal S3 object interface while older versions remain available.

Removing the Delete Marker can make the previous object version visible again.

## Permanent Deletion

To permanently remove a particular version, the specific Version ID must be supplied:

``powershell
aws s3api delete-object ` 
  --bucket <bucket-name> ` 
  --key <object-key> ` 
  --version-id <version-id>
``

## Cost-Control Lesson

S3 Versioning can retain older object versions even when the current object appears deleted.

For production environments, lifecycle policies should be considered to automatically manage old object versions, Delete Markers, incomplete multipart uploads, and storage-class transitions.

## Lab Completion

The complete test bucket and all associated object versions were cleaned up and the bucket was deleted after the exercise.

**Lab Status: Completed**
