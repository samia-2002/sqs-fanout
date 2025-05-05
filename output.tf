output "input_bucket_name" {
  value = aws_s3_bucket.picture_bucket.id  
}

output "output_bucket_name" {
  value = aws_s3_bucket.output_bucket.id 
}

output "lambda_function_name" {
  value = aws_lambda_function.lambda_function.function_name  

}

output "sqs_queue_url" {
  value = aws_sqs_queue.subscribe_picture.url  
}
