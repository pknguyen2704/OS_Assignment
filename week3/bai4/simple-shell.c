/**
 * Simple shell interface program.
 *
 * Operating System Concepts - Tenth Edition
 * Copyright John Wiley & Sons - 2018
 */

 #include <stdio.h>
 #include <stdlib.h>
 #include <string.h>
 #include <unistd.h>
 #include <sys/types.h>
 #include <sys/wait.h>
 #include <fcntl.h>
 
 #define MAX_LINE 80
 
 int main(void) {
     char *args[MAX_LINE / 2 + 1];
     char last_command[MAX_LINE] = "";
     int should_run = 1; /* Cờ kiểm soát vòng lặp */
 
     while (should_run) {
         printf("osh> ");
         fflush(stdout);
 
         char input[MAX_LINE];
         if (fgets(input, MAX_LINE, stdin) == NULL) continue; // Đọc input
         input[strcspn(input, "\n")] = 0;
 
         if (strcmp(input, "exit") == 0) break; // type "exit" 2exit shell
 
         // Hỗ trợ !! để chạy lệnh trước đó
         if (strcmp(input, "!!") == 0) {
             if (strlen(last_command) == 0) {
                 printf("No commands in history\n");
                 continue;
             }
             strcpy(input, last_command);
             printf("%s\n", input);
         } else {
             strcpy(last_command, input);
         }
 
         // Tách input thành các token
         char *token = strtok(input, " ");
         int i = 0;
         while (token != NULL) {
             args[i++] = token;
             token = strtok(NULL, " ");
         }
         args[i] = NULL;
 
         if (i == 0) continue; // Không có lệnh hợp lệ
 
         // Kiểm tra chạy nền (&)
         int background = 0;
         if (strcmp(args[i - 1], "&") == 0) {
             background = 1;
             args[i - 1] = NULL; // Xóa '&' khỏi danh sách lệnh
             i--;
         }
 
         // Kiểm tra có redirection hoặc pipe
         int out_redirect = 0, in_redirect = 0, has_pipe = 0;
         char *out_file = NULL, *in_file = NULL;
         char *left_args[MAX_LINE], *right_args[MAX_LINE];
 
         for (int j = 0; j < i; j++) {
             if (strcmp(args[j], ">") == 0) {
                 out_redirect = 1;
                 out_file = args[j + 1];
                 args[j] = NULL;
             } else if (strcmp(args[j], "<") == 0) {
                 in_redirect = 1;
                 in_file = args[j + 1];
                 args[j] = NULL;
             } else if (strcmp(args[j], "|") == 0) {
                 has_pipe = 1;
                 args[j] = NULL;
                 
                 for (int k = 0; k < j; k++) left_args[k] = args[k];
                 left_args[j] = NULL;
                 for (int k = j + 1; k < i; k++) right_args[k - j - 1] = args[k];
                 right_args[i - j - 1] = NULL;
                 break;
             }
         }
 
         if (has_pipe) { // Xử lý pipe
             int pipe_fd[2];
             pipe(pipe_fd);
             pid_t pid1 = fork();
             if (pid1 == 0) {
                 dup2(pipe_fd[1], STDOUT_FILENO);
                 close(pipe_fd[0]);
                 close(pipe_fd[1]);
                 execvp(left_args[0], left_args);
                 perror("exec failed");
                 exit(1);
             }
 
             pid_t pid2 = fork();
             if (pid2 == 0) {
                 dup2(pipe_fd[0], STDIN_FILENO);
                 close(pipe_fd[0]);
                 close(pipe_fd[1]);
                 execvp(right_args[0], right_args);
                 perror("exec failed");
                 exit(1);
             }
 
             close(pipe_fd[0]);
             close(pipe_fd[1]);
             wait(NULL);
             wait(NULL);
             continue;
         }
 
         // Tạo tiến trình con để thực thi lệnh
         pid_t pid = fork();
         if (pid == 0) {
             if (out_redirect) {
                 int fd = open(out_file, O_WRONLY | O_CREAT | O_TRUNC, 0644);
                 dup2(fd, STDOUT_FILENO);
                 close(fd);
             }
             if (in_redirect) {
                 int fd = open(in_file, O_RDONLY);
                 dup2(fd, STDIN_FILENO);
                 close(fd);
             }
             execvp(args[0], args);
             perror("exec failed");
             exit(1);
         } else if (!background) {
             wait(NULL);
         }
     }
     return 0;
 }
 
 